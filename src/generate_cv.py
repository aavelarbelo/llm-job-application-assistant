"""
generate_cv.py: build a 1-page, ATS-friendly CV from the master profile.

The point of this script is that **only verified facts can reach the CV**:

  1. It parses the master profile (Markdown) into facts, each with an ID and a status:
     VERIFIED, FORBIDDEN or TO CONFIRM.
  2. A "variant" (JSON) lists which fact IDs go into the CV and in what order.
     The variant contains no free text, only IDs.
  3. Validation fails if a variant uses an ID that is unknown, forbidden or still to confirm,
     or if a verified fact has no source.
  4. The final text is scanned for the FORBIDDEN patterns (e.g. an unproven "30%").
  5. The CV is written with python-docx, converted to PDF with LibreOffice and must be exactly
     1 page (checked with pypdf).

Usage:
    python src/generate_cv.py \
        --profile knowledge-base/master-profile.example.md \
        --variant src/variants/data-analyst.json \
        --company ExampleCorp \
        --out output/
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.shared import Cm, Pt
from pypdf import PdfReader

# --------------------------------------------------------------------------------------
# 1. Parsing the master profile
# --------------------------------------------------------------------------------------

# "- **F-101** Some fact text — _source: reference letter_"
FACT_RE = re.compile(r"^- \*\*([A-Z]+-\d+)\*\*\s+(.*)$")
# "#### EXP-01 | Sales Analyst | Acme Components Lda. | Jan 2019 – Mar 2023"
ENTRY_RE = re.compile(r"^#### ([A-Z]+-\d+)\s*\|(.*)$")
# The source is written at the end of a fact, after an em dash.
SOURCE_RE = re.compile(r"\s+—\s+_source:\s*(.*?)_\s*$")
# Forbidden patterns are written in backticks: Patterns: `30%`, `AWS`
PATTERN_RE = re.compile(r"`([^`]+)`")


@dataclass
class Item:
    """A fact or an entry (job, project, degree) from the master profile."""

    id: str
    text: str
    status: str  # "verified" | "forbidden" | "to_confirm"
    category: str = ""  # header, summary, skills, experience, projects, education, languages
    source: str = ""
    parent: str = ""  # for facts that belong to an entry, e.g. F-101 -> EXP-01
    fields: list[str] = field(default_factory=list)  # entry columns: title, org, dates
    patterns: list[str] = field(default_factory=list)  # only for forbidden items


def parse_profile(path: Path) -> dict[str, Item]:
    """Read the master profile and return {id: Item}."""
    items: dict[str, Item] = {}
    status = ""  # set by the "## ..." headings
    category = ""  # set by the "### ..." headings
    current_entry: Item | None = None

    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()

        # "## VERIFIED FACTS", "## FORBIDDEN", "## TO CONFIRM": anything else is ignored.
        if line.startswith("## "):
            title = line[3:].upper()
            status = (
                "verified" if "VERIFIED" in title
                else "forbidden" if "FORBIDDEN" in title
                else "to_confirm" if "TO CONFIRM" in title
                else ""
            )
            category, current_entry = "", None
            continue

        if not status:
            continue  # intro text, tables, update log...

        if line.startswith("### "):
            # "### Summary sentences" -> "summary"
            category = line[4:].split()[0].lower()
            current_entry = None
            continue

        entry = ENTRY_RE.match(line)
        if entry:
            fields = [f.strip() for f in entry.group(2).split("|")]
            current_entry = Item(id=entry.group(1), text=fields[0], status=status,
                                 category=category, fields=fields)
            items[current_entry.id] = current_entry
            continue

        # Entries have their source on the line below the heading.
        if current_entry and line.startswith("_source:"):
            current_entry.source = line.removeprefix("_source:").strip(" _")
            continue

        fact = FACT_RE.match(line)
        if fact:
            fact_id, text = fact.groups()
            item = Item(id=fact_id, text=text, status=status, category=category,
                        parent=current_entry.id if current_entry else "")
            source = SOURCE_RE.search(text)
            if source:
                item.source = source.group(1).strip()
                item.text = text[: source.start()].strip()
            if status == "forbidden":
                item.patterns = PATTERN_RE.findall(text)
            items[fact_id] = item

    return items


# --------------------------------------------------------------------------------------
# 2. Validation: the guardrail
# --------------------------------------------------------------------------------------

def variant_ids(variant: dict) -> list[str]:
    """Every fact/entry ID that a variant wants to use (header facts are always used)."""
    ids: list[str] = []
    for key in ("summary", "skills", "languages"):
        ids += variant.get(key, [])
    for key in ("experience", "projects", "education"):
        for entry_id, fact_ids in variant.get(key, {}).items():
            ids += [entry_id, *fact_ids]
    return ids


def validate(variant: dict, items: dict[str, Item]) -> list[str]:
    """Return a list of human-readable errors. An empty list means the variant is safe."""
    errors = []

    # Every verified fact must say where it comes from.
    for item in items.values():
        if item.status == "verified" and not item.source:
            errors.append(f"{item.id}: verified fact without a source")

    for item_id in variant_ids(variant):
        item = items.get(item_id)
        if item is None:
            errors.append(f"{item_id}: not in the master profile")
        elif item.status == "forbidden":
            errors.append(f"{item_id}: FORBIDDEN fact ({item.text})")
        elif item.status == "to_confirm":
            errors.append(f"{item_id}: still TO CONFIRM, cannot be used ({item.text})")

    # A bullet must belong to the entry it is listed under (no moving a project bullet into
    # a job, which would turn academic work into professional experience).
    for key in ("experience", "projects", "education"):
        for entry_id, fact_ids in variant.get(key, {}).items():
            for fact_id in fact_ids:
                fact = items.get(fact_id)
                if fact and fact.status == "verified" and fact.parent != entry_id:
                    errors.append(f"{fact_id}: belongs to {fact.parent or 'no entry'}, "
                                  f"not to {entry_id}")
    return errors


def scan_forbidden(text: str, items: dict[str, Item]) -> list[str]:
    """Second line of defence: look for forbidden patterns in the final CV text."""
    hits = []
    for item in items.values():
        for pattern in item.patterns:
            if re.search(re.escape(pattern), text, flags=re.IGNORECASE):
                hits.append(f'{item.id}: found forbidden pattern "{pattern}"')
    return hits


# --------------------------------------------------------------------------------------
# 3. Building the DOCX
# --------------------------------------------------------------------------------------

FONT = "Calibri"
SIZE = Pt(10.5)


def _paragraph(doc, text="", bold=False, size=SIZE, align=WD_ALIGN_PARAGRAPH.JUSTIFY,
               space_after=Pt(1)):
    """Add a plain paragraph with consistent spacing."""
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_after = space_after
    p.paragraph_format.space_before = Pt(0)
    if text:
        run = p.add_run(text)
        run.bold, run.font.size, run.font.name = bold, size, FONT
    return p


def _section_title(doc, title: str):
    """Section titles: capitals, bold, left-aligned (no tables or columns, for ATS)."""
    p = _paragraph(doc, title.upper(), bold=True, size=Pt(11),
                   align=WD_ALIGN_PARAGRAPH.LEFT, space_after=Pt(1))
    p.paragraph_format.space_before = Pt(5)


def _bullet(doc, text: str):
    p = doc.add_paragraph(style="List Bullet")
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_after = Pt(0)
    run = p.add_run(text)
    run.font.size, run.font.name = SIZE, FONT


def _entry_line(doc, entry: Item):
    """'Title | Organisation' on the left, dates on the right (right-aligned tab stop)."""
    title, org, dates = (entry.fields + ["", "", ""])[:3]
    p = _paragraph(doc, align=WD_ALIGN_PARAGRAPH.LEFT, space_after=Pt(0))
    p.paragraph_format.space_before = Pt(2)
    usable_width = doc.sections[0].page_width - doc.sections[0].left_margin \
        - doc.sections[0].right_margin
    p.paragraph_format.tab_stops.add_tab_stop(usable_width, WD_TAB_ALIGNMENT.RIGHT)
    for text, bold in ((title, True), (f" | {org}", False), (f"\t{dates}", False)):
        run = p.add_run(text)
        run.bold, run.font.size, run.font.name = bold, SIZE, FONT


def _label_line(doc, text: str):
    """'Label: values' with the label in bold (used for skills and languages)."""
    label, _, rest = text.partition(":")
    p = _paragraph(doc, space_after=Pt(0))
    for chunk, bold in ((label + (":" if rest else ""), True), (rest, False)):
        run = p.add_run(chunk)
        run.bold, run.font.size, run.font.name = bold, SIZE, FONT


def build_docx(variant: dict, items: dict[str, Item], company: str) -> Document:
    doc = Document()

    # Narrow margins and a single column.
    section = doc.sections[0]
    section.page_height, section.page_width = Cm(29.7), Cm(21.0)  # A4
    for side in ("top_margin", "bottom_margin"):
        setattr(section, side, Cm(1.3))
    for side in ("left_margin", "right_margin"):
        setattr(section, side, Cm(1.6))

    # Header: name, then location + work authorisation, then contacts.
    header = {i.id: i.text for i in items.values() if i.category == "header"}
    _paragraph(doc, header.get("H-01", ""), bold=True, size=Pt(16),
               align=WD_ALIGN_PARAGRAPH.CENTER, space_after=Pt(0))
    _paragraph(doc, f"{variant['target_title']} · {header.get('H-02', '')} · "
                    f"{header.get('H-04', '')}",
               align=WD_ALIGN_PARAGRAPH.CENTER, space_after=Pt(0))
    _paragraph(doc, header.get("H-03", ""), align=WD_ALIGN_PARAGRAPH.CENTER,
               space_after=Pt(2))

    # Sections, in the order the variant asks for.
    for name in variant["section_order"]:
        if name == "summary":
            _section_title(doc, "Summary")
            _paragraph(doc, " ".join(items[i].text for i in variant["summary"]))
        elif name in ("skills", "languages"):
            _section_title(doc, name)
            for item_id in variant[name]:
                _label_line(doc, items[item_id].text)
        elif name in ("experience", "projects", "education"):
            _section_title(doc, name)
            for entry_id, fact_ids in variant[name].items():
                _entry_line(doc, items[entry_id])
                for fact_id in fact_ids:
                    _bullet(doc, items[fact_id].text)

    # File metadata (read by some ATS and visible in file properties).
    props = doc.core_properties
    props.author = header.get("H-01", "")
    props.title = f"CV - {props.author} - {variant['target_title']} - {company}"
    props.keywords = ", ".join(variant.get("keywords", []))
    return doc


def docx_text(doc: Document) -> str:
    return "\n".join(p.text for p in doc.paragraphs)


# --------------------------------------------------------------------------------------
# 4. PDF conversion and the 1-page check
# --------------------------------------------------------------------------------------

def convert_to_pdf(docx_path: Path) -> Path:
    """Convert with LibreOffice in headless mode; the PDF is written next to the DOCX."""
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if not soffice:
        sys.exit("LibreOffice not found (need 'soffice' on PATH). Use --no-pdf to skip.")
    subprocess.run([soffice, "--headless", "--convert-to", "pdf", "--outdir",
                    str(docx_path.parent), str(docx_path)],
                   check=True, capture_output=True, timeout=120)
    return docx_path.with_suffix(".pdf")


def page_count(pdf_path: Path) -> int:
    return len(PdfReader(pdf_path).pages)


# --------------------------------------------------------------------------------------
# 5. CLI
# --------------------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    parser.add_argument("--profile", type=Path, required=True, help="master profile (.md)")
    parser.add_argument("--variant", type=Path, required=True, help="variant (.json)")
    parser.add_argument("--company", default="ExampleCorp", help="used in file name/metadata")
    parser.add_argument("--out", type=Path, default=Path("output"))
    parser.add_argument("--no-pdf", action="store_true", help="skip PDF conversion")
    args = parser.parse_args()

    items = parse_profile(args.profile)
    variant = json.loads(args.variant.read_text(encoding="utf-8"))
    verified = sum(i.status == "verified" for i in items.values())
    print(f"Profile: {verified} verified items, "
          f"{sum(i.status == 'forbidden' for i in items.values())} forbidden, "
          f"{sum(i.status == 'to_confirm' for i in items.values())} to confirm")

    errors = validate(variant, items)
    if errors:
        print("\nVariant rejected:\n  - " + "\n  - ".join(errors))
        return 1

    doc = build_docx(variant, items, args.company)
    hits = scan_forbidden(docx_text(doc), items)
    if hits:
        print("\nForbidden content found:\n  - " + "\n  - ".join(hits))
        return 1

    # File name: CV_[Company]_[YYYY-MM]_[variant]
    args.out.mkdir(parents=True, exist_ok=True)
    stem = f"CV_{args.company}_{date.today():%Y-%m}_{variant['variant']}"
    docx_path = args.out / f"{stem}.docx"
    doc.save(docx_path)
    print(f"DOCX: {docx_path}")

    if not args.no_pdf:
        pdf_path = convert_to_pdf(docx_path)
        pages = page_count(pdf_path)
        print(f"PDF:  {pdf_path} ({pages} page{'s' if pages != 1 else ''})")
        if pages != 1:
            print("CV is longer than 1 page: remove facts from the variant.")
            return 1

    # Remind the user what was left out on purpose.
    pending = [i for i in items.values() if i.status == "to_confirm"]
    if pending:
        print("\nTO CONFIRM (not used):")
        for item in pending:
            print(f"  - {item.id}: {item.text}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
