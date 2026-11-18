# Lessons learned: real errors and the rules that prevent them

Each case below happened while I was using the system for real applications. Where a detail
would expose my personal data, it is described in general terms or replaced with the fictional
"Jane Doe" equivalent from
[`../knowledge-base/master-profile.example.md`](../knowledge-base/master-profile.example.md).

The common thread: **wrong or unsupported information gets reused.** The fix is never "ask the
model to be more careful". It is to make the fact explicit, forbid the wrong version, fix the
source, or check it in code.

---

## 1. Unverified numbers in older CV versions

**What happened.** Older versions of my CV and related texts contained numbers I could not
back up with any document: page counts and record totals from a group project, and a
percentage attributed to a previous role. The unverified numbers came from older CV versions
used as templates; the forbidden-facts list was created so they could never reappear.

**Why it matters.** A number in a CV is a claim that can be questioned in an interview. If
there is no source for it, it is a liability, not an asset.

**Rules that now prevent it.**
- The master profile is the **single source of facts**; older CVs are only templates for format
  and wording (`prompts/project-system-prompt.md`).
- Every verified fact needs a `source`; the CV generator rejects verified facts without one.
- Unproven claims are listed in a **FORBIDDEN** section, by name, so the model is told what it
  must *not* say as well as what to say.
- Forbidden items carry text patterns (Jane Doe example: `30%`), and `src/generate_cv.py` scans
  every generated CV for them as a final check.

## 2. An unfinished master's recorded as a degree in my own public profile

**What happened.** LinkedIn's job-matching feature showed me insights like *"34% have a
Master's degree (similar to you)"*. The reason was my own profile: a master's programme I
started but did not complete was registered as a "Master's degree". No model misread anything:
the source data itself (my public profile) was inconsistent with reality.

**Why it matters.** Any system that reads that profile, whether a recruiter's ATS, LinkedIn's
own matching or an LLM, would conclude that I hold a degree I don't have. Claiming a degree you
don't have is the kind of error that ends a recruitment process.

**What I changed.** I fixed the source, not the model output:
- The public profile now shows the programme as not completed.
- In the master profile, the education entry states its status in the title itself (Jane Doe:
  *"MSc in Operations Research (not completed)"*), plus a separate fact: *"Programme not
  completed; no degree awarded."*
- "A completed master's degree" is in the FORBIDDEN list.
- The form-filling prompt has an explicit answer for "Do you have a master's?": the programme
  name, followed by *NOT completed*.

## 3. Application forms that reject LLM-generated text

**What happened.** Text that was correct and well written still failed in real forms:
- **(a) Special characters.** A portal rejected descriptions containing characters such as `±`
  and `<`, with the error *"Enter a valid string"*.
- **(b) Numeric-only fields.** A salary field only accepted numbers; free text (the
  standard salary-expectation sentence) returned *"Valor inválido"* ("Invalid value").
- **(c) Character limits.** Messages limited to 300 or 400 characters.

**Why it matters.** An answer in the wrong format either blocks the form or gets silently cut.

**Rules that now prevent it.**
- A reusable **answers sheet** (`tracking/answers-sheet.example.md`) keeps, for each common
  question, a free-text answer (PT/EN) and a numeric range for fields that only accept numbers.
- The form-filling agent may only use the listed data and must **stop and ask** if a field
  wants something that isn't there, instead of reformatting or inventing.
- Recruiter messages have an explicit character limit (300) in the system prompt.

**Lesson:** outputs must be adapted to the target system, not just generated.

---

## Other rules in the profile that follow the same pattern

The real FORBIDDEN list also covers these categories of tempting overstatement. They are listed
as rules, not as incidents:

- **Group work presented as individual work.** For group projects, only my own part is listed,
  with fixed bullets; group totals are forbidden.
- **Inflated job titles.** The CV uses the title from the employment contract.
- **Tools seen only in coursework presented as practical skills** (e.g. cloud platforms).
  Skills are split into practical, coursework only and in progress.
- **Academic projects presented as professional experience.** The CV generator rejects any
  project bullet placed under a job entry.
- **Empty self-praise** ("passionate", "highly motivated").
