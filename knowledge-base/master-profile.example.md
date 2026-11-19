# Master Profile: Andressa Avelar Belo (public version)

> **Public version of my real master profile.** It contains only facts that are already public
> on my CV and LinkedIn. The private version also holds contact details and internal notes
> (claims I removed from old CVs and why, interview notes); those are not published.

This file is the **single source of truth** for every CV, cover letter, recruiter message and
form answer. The LLM may reorder facts and adapt wording to a job posting's vocabulary, but it
may **not add** anything that is not here.

**Version:** v6 (public) · **Last updated:** 2026-11

## How this file is structured

| Section | Can it be used? | Format |
|---|---|---|
| `VERIFIED FACTS` | Yes | Every fact has an ID in bold and a `_source:_` |
| `FORBIDDEN` | Never | Claims that are tempting but not true for me. `Patterns` are scanned automatically in generated CVs |
| `TO CONFIRM` | Not yet | Possibly true, but no document yet. Listed at the end of each output, never used in it |

Entries (jobs, projects, degrees) use `#### ID | Title | Organisation | Dates`.
Facts use `- **ID** text — _source: ..._`. `src/generate_cv.py` parses exactly this format.

---

## VERIFIED FACTS

### Header

- **H-01** Andressa Avelar Belo — _source: ID document_
- **H-02** Porto, Portugal — _source: proof of address_
- **H-03** linkedin.com/in/andressaavelar · github.com/aavelarbelo — _source: own accounts_
- **H-04** Authorised to work in Portugal — _source: residence document_

### Summary sentences

Pre-validated sentences. The LLM picks and orders them; it does not write new claims.

- **SUM-01** Junior Data Engineer with a Control & Automation Engineering background and a postgraduate qualification in Big Data & Decision Making (ISEP, 2026). — _source: EDU-01, EDU-02_
- **SUM-02** Hands-on with Python, SQL and PostgreSQL through academic projects covering web scraping, data cleaning, data quality checks and Power BI. — _source: PRJ-01_
- **SUM-03** 4+ years in an electrical engineering company working with cost estimates, sales KPIs and project data, plus experimental data analysis as a research fellow at INEGI. — _source: EXP-01, EXP-02_
- **SUM-04** Currently completing a data engineering bootcamp (Airflow, Snowflake, dbt). — _source: course enrolment (in progress)_

### Skills

- **SK-01** Data engineering (postgraduate and project level): Python, SQL, PostgreSQL, ETL, data quality, web scraping (Selenium) — _source: PRJ-01 repository_
- **SK-02** BI & reporting: Power BI, Excel — _source: PRJ-01, EXP-01_
- **SK-03** Tools: Git/GitHub, Docker, Jupyter, Microsoft SQL Server, n8n, Claude API — _source: PRJ-01, PRJ-02 repositories_
- **SK-04** Coursework only (no practical use): Data Warehousing, Spark, Kafka, NoSQL (MongoDB, Cassandra, Redis), Scikit-learn — _source: EDU-01 syllabus_
- **SK-05** In progress: Airflow, Snowflake, dbt (bootcamp) — _source: course enrolment_
- **SK-06** Methods: statistical analysis (t-tests), image analysis (ImageJ), GraphPad Prism, MATLAB — _source: EXP-02_

### Experience

#### EXP-02 | Research Fellow (SPINMESH project) | INEGI, Porto | Jul 2021 – Dec 2021
_source: official declaration_

- **F-111** Contributed experimental data from uniaxial tensile tests to the team's study comparing a 3D-printed biodegradable PCL mesh with a commercial polypropylene mesh; quantified pore deformation through image analysis in ImageJ. — _source: CNME 2020 paper_
- **F-112** Statistical analysis in GraphPad Prism and Excel (t-tests, mean ± SEM, p < 0.05); co-authored 3 scientific works, including an oral presentation at the 12th National Congress of Experimental Mechanics. — _source: CNME 2020 paper (DOI 10.25766/vnbn-a964)_

#### EXP-01 | Engineering Assistant (Projects, Field Operations & Data Analysis) | SIEL Engenharia, Belém, Brazil | Jan 2018 – Jul 2019
_source: reference from my direct supervisor; earlier roles at the same company: Engineering Intern (2015), Technical Training & Administrative Assistant (2016–2017)_

- **F-101** Tracked sales KPIs against quarterly targets. — _source: reference_
- **F-102** Prepared technical and commercial proposals for clients, including consulting in other states. — _source: reference_
- **F-103** Prepared cost estimates for electrical works from project drawings (quantities, materials, labour, costs). — _source: reference_

### Projects

Projects are **academic or personal**. They are never presented as professional experience.

#### PRJ-01 | UrbanEco Analytics (academic, group project, 16/20) | ISEP, Porto | 2026
_source: graded project; only my own part is listed_

- **F-201** Developed a Python/Selenium scraper with automatic pagination to collect property listings, and validated the collection by URL, which revealed repeated results across pages. — _source: project repository_
- **F-202** Wrote the cleaning script in Python/pandas (price-per-m² filters, duplicate removal) and set up a local PostgreSQL database in Docker to load and query the cleaned data. — _source: project repository_
- **F-203** Reviewed the team's Power BI dashboard and fixed a KPI that summed segments (14,772 → 338 €/m²), the handling of missing values and the logic of two rankings. — _source: project report_

#### PRJ-02 | LLM Job Application Assistant (personal project) | this repository | 2026
_source: this repository_

- **F-211** Built a daily n8n workflow that screens LinkedIn job alerts with a free rule-based filter and the Claude API, returns structured JSON and logs every result in Google Sheets. — _source: n8n/ folder_
- **F-212** Tested it with real postings and fixed reliability issues (truncated responses, invented commitments, silent failures). — _source: README, docs/lessons-learned.md_

### Education

#### EDU-01 | Postgraduate Programme in Big Data & Decision Making | ISEP, Porto | Nov 2025 – Jun 2026
_source: transcript_

- **F-301** Average grade: 15/20. — _source: transcript_

#### EDU-03 | MSc in Computational Mechanics (not completed) | FEUP, Porto | 2020 – 2022
_source: enrolment certificate_

- **F-311** Programme not completed; no degree awarded. — _source: enrolment certificate_

#### EDU-02 | BSc in Control & Automation Engineering | Estácio/IESAM, Belém, Brazil | 2014 – 2019
_source: diploma_

### Languages

- **LANG-01** Portuguese: native — _source: nationality_
- **LANG-02** English: B2 (upper intermediate) — _source: self-assessment; certificate planned_

---

## FORBIDDEN

Never use these, in any wording. These are the honest limits of my profile: things an LLM tends
to add because they are common in data CVs, but that are not true for me.

- **X-01** Cloud platforms as a practical skill (only seen in coursework). Patterns: `Azure`, `GCP`
- **X-02** Star schema / dimensional modelling: studied, never applied in a project. Patterns: `star schema`, `dimensional model`
- **X-03** Tableau: never used. Patterns: `Tableau`
- **X-04** A completed master's degree (EDU-03 was not completed). Patterns: `Master's degree`, `MSc graduate`
- **X-05** Professional data experience: all data projects are academic or personal. Patterns: `years of experience as a data`
- **X-06** Empty self-praise. Patterns: `passionate`, `highly motivated`

---

## TO CONFIRM

Listed at the end of each output under "TO CONFIRM", never used in a CV.

- **C-01** English level to declare: certificate planned for December 2026.
- **C-02** Cost per posting of the n8n workflow after the November fixes: not measured yet.

---

## UPDATE LOG

- **v6 (2026-11):** public version published with the repository.
