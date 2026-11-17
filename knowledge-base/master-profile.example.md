# Master Profile: Jane Doe (EXAMPLE)

> **Fictional person.** This file shows the *structure* of the real master profile used by the
> system. Every name, institution, company, date and number below is invented.

This file is the **single source of truth** for every CV, cover letter, recruiter message and
form answer. The LLM may reorder facts and adapt wording to a job posting's vocabulary, but it
may **not add** anything that is not here.

**Version:** v1 (example) · **Last updated:** 2026-11

## How this file is structured

| Section | Can it be used? | Format |
|---|---|---|
| `VERIFIED FACTS` | Yes | Every fact has an ID in bold and a `_source:_` |
| `FORBIDDEN` | Never | Claims that appeared in old CVs or LLM drafts but cannot be proven. `Patterns` are scanned automatically in generated CVs |
| `TO CONFIRM` | Not yet | Possibly true, but no document yet. Listed at the end of each output, never used in it |

Entries (jobs, projects, degrees) use `#### ID | Title | Organisation | Dates`.
Facts use `- **ID** text — _source: ..._`. `src/generate_cv.py` parses exactly this format.

---

## VERIFIED FACTS

### Header

- **H-01** Jane Doe — _source: ID document_
- **H-02** Lisbon, Portugal — _source: proof of address_
- **H-03** jane.doe@example.com · +351 000 000 000 · linkedin.com/in/jane-doe-example — _source: own accounts_
- **H-04** Authorised to work in Portugal — _source: residence permit_

### Summary sentences

Pre-validated sentences. The LLM picks and orders them; it does not write new claims.

- **SUM-01** Career changer into data with a postgraduate diploma in Data Analytics and six years of business experience in sales reporting and operations. — _source: EDU-01, EXP-01, EXP-02_
- **SUM-02** Hands-on with Python, SQL and Power BI through academic projects covering ETL, data quality checks and dashboards. — _source: PRJ-01, PRJ-02_
- **SUM-03** Used to turning sales and operations data into recurring reports for non-technical teams. — _source: F-101, F-111_
- **SUM-04** Currently completing a data engineering bootcamp (Airflow, dbt, Snowflake). — _source: enrolment confirmation (in progress)_

### Skills

- **SK-01** Programming & data: Python (pandas), SQL (PostgreSQL), ETL, data quality checks — _source: PRJ-01, PRJ-02_
- **SK-02** BI & reporting: Power BI, Excel (pivot tables, Power Query) — _source: PRJ-01, EXP-01_
- **SK-03** Tools: Git, Docker, Jupyter — _source: PRJ-01 repository_
- **SK-04** Coursework only (no practical use): Spark, Kafka, NoSQL — _source: EDU-01 syllabus_
- **SK-05** In progress: Airflow, dbt, Snowflake (bootcamp) — _source: enrolment confirmation_
- **SK-06** Methods: descriptive statistics, process documentation — _source: EDU-01, F-112_

### Experience

#### EXP-02 | Operations Assistant | Bluebird Logistics | Apr 2023 – Sep 2025
_source: employment contract_

- **F-111** Tracked daily shipment exceptions in a shared spreadsheet and reported recurring causes to the shift lead every week. — _source: reference letter_
- **F-112** Wrote the step-by-step returns-handling procedure used to onboard new team members. — _source: procedure document (own authorship)_

#### EXP-01 | Sales Analyst | Acme Components Lda. | Jan 2019 – Mar 2023
_source: employment contract_

- **F-101** Prepared weekly sales KPI reports in Excel for the commercial team. — _source: reference letter_
- **F-102** Prepared quotes for industrial clients, cross-checking prices against ERP exports. — _source: job description_
- **F-103** Consolidated the customer list from three separate spreadsheets into one shared file. — _source: reference letter_

### Projects

All projects are **academic**. They are never presented as professional experience.

#### PRJ-01 | Retail Sales ETL Pipeline (academic, individual) | Example Polytechnic Institute | 2026
_source: graded project report_

- **F-201** Built a Python ETL pipeline that loads public retail sales data (CSV) into PostgreSQL. — _source: project repository_
- **F-202** Implemented data quality checks for nulls, duplicates and invalid dates before loading. — _source: project repository_
- **F-203** Built a Power BI report on the PostgreSQL tables showing monthly sales and returns. — _source: project report_

#### PRJ-02 | GreenCity Urban Mobility Analysis (academic, group of 4) | Example Polytechnic Institute | 2026
_source: graded project report; only my own part is listed_

- **F-211** Cleaned and merged public bike-sharing and weather datasets in Python (pandas). — _source: contribution table in the report_
- **F-212** Wrote the SQL queries used in the station-level usage analysis. — _source: contribution table in the report_

### Education

#### EDU-01 | Postgraduate Diploma in Data Analytics | Example Polytechnic Institute | Oct 2025 – Jun 2026
_source: diploma_

- **F-301** Average grade: 16/20. — _source: transcript_

#### EDU-03 | MSc in Operations Research (not completed) | Example University | 2018 – 2019
_source: enrolment certificate_

- **F-311** Programme not completed; no degree awarded. — _source: enrolment certificate_

#### EDU-02 | BSc in Industrial Engineering | Example University | 2014 – 2018
_source: diploma_

### Languages

- **LANG-01** Portuguese: native — _source: nationality_
- **LANG-02** English: B2 (upper intermediate) — _source: language certificate_

---

## FORBIDDEN

Never use these, in any wording. Each one either appeared in an old CV / LLM draft or is a
tempting exaggeration.

- **X-01** "Reduced quoting time by 30%" at Acme: appeared in an old CV, never measured. Patterns: `30%`
- **X-02** GreenCity group totals presented as personal work (e.g. "analysed 1.2M trips"). Patterns: `1.2M`, `1,200,000`
- **X-03** "Engineer" as a job title at Acme (the real title is Sales Analyst). Patterns: `Sales Engineer`
- **X-04** Cloud platforms as a practical skill (only seen in coursework). Patterns: `AWS`, `Azure`, `GCP`
- **X-05** Star schema / dimensional modelling: one lecture, never applied. Patterns: `star schema`, `dimensional model`
- **X-06** Tableau: never used. Patterns: `Tableau`
- **X-07** A completed master's degree (EDU-03 was not completed). Patterns: `Master's degree`, `MSc graduate`
- **X-08** Empty self-praise. Patterns: `passionate`, `highly motivated`

---

## TO CONFIRM

Listed at the end of each output under "TO CONFIRM", never used in a CV.

- **C-01** Final grade of the postgraduate thesis: waiting for the official transcript.
- **C-02** Size of the consolidated customer list at Acme: no document confirms the number.
- **C-03** Power BI certification: exam booked, not yet passed.

---

## UPDATE LOG

- **v1 (2026-11):** example created for the public repository.
