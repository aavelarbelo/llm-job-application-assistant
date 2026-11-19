# Job screening prompt (browser agent, read-only)

**Used with:** Claude in Chrome, on one LinkedIn job-search results tab at a time.

**Input:** an open results page. **Output:** a ranked table of the jobs worth applying to, a
one-line summary of discards and the full description of each shortlisted job (to paste into
the project in `project-system-prompt.md`).

> Translated from Portuguese. The profile summary is my own (public facts only). The rules,
> limits and forbidden actions are unchanged.

Design notes:
- **Read-only by design.** The agent may click through the list and "see more", but the
  forbidden actions are listed explicitly (apply, save, message, close tabs).
- **Bounded run.** It stops after 3 pages or 75 jobs, so a run can't go on indefinitely.
- **The profile is restated inline, with "don't assume anything else"**, because the agent
  only sees this prompt, not the master profile.

---

```text
JOB SCREENING — ONLY IN THIS TAB (the one open now). Read-only.

This page is a list of LinkedIn job results. I want you to go through ALL jobs on this list, one
by one:
1. In the left column, click the 1st job. Read the right panel (title, company, location,
   work mode and the "About the job" section; click "see more" if it exists).
2. Apply the rules below and decide: WORTH IT or NOT WORTH IT.
3. Move to the next job. Scroll the left column to load more jobs.
4. When you finish the page, click "Next" and continue. Stop at the end of page 3 or when you
   have seen 75 jobs.
5. Skip jobs already marked "Applied" and duplicates.

MY PROFILE (don't assume anything else):
- BSc in Control & Automation Engineering (2019) + postgraduate programme in Big Data &
  Decision Making (ISEP, 2026).
- Data: 0 professional years; academic and personal projects only. I know Python, SQL,
  PostgreSQL, ETL, data quality, Power BI, Excel, Git, Docker. Coursework only, no practice:
  Spark, Kafka, NoSQL. In progress: Airflow, Snowflake, dbt.
- 4+ years in an electrical engineering company (cost estimates, sales KPIs, proposals) and
  experimental data analysis as a research fellow.
- Portuguese native, English B2. No French, German or Spanish.
- I live in Porto. Authorised to work in Portugal.
- Interests: data engineering, BI, applied AI, engineering and energy.

NOT WORTH IT if:
- It asks for 3+ years of experience, or 1+ year of mandatory professional experience in the role.
- It requires a mandatory tool I don't have (Databricks, PySpark, hands-on Azure/AWS/GCP,
  Dataiku, Ab Initio, SAP, mandatory Tableau, ML in production).
- It requires French/German/another language, English C1, or a master's degree.
- It is senior, lead, manager, or in another field.
- It is outside commuting distance, EXCEPT a trainee/junior role at a top company that is an
  almost perfect fit.
- It says it is "no longer accepting applications".

WORTH IT if: it is junior/trainee/internship/graduate (or no years required), in Porto and
surroundings or remote in Portugal, and I meet about 60% of the mandatory requirements.

FORBIDDEN: applying, clicking "Apply"/"Easy Apply", saving jobs, sending messages or closing tabs.

RESULT (only at the end):
A) Table ONLY with the jobs that are WORTH IT, best to worst:
   | Score 0-10 | Company | Role | Location / mode | Why it's worth it (1 line) | Main gap | Job link |
B) One line: "Saw X jobs; Y worth it; Z discarded" + the 3 most common discard reasons.
C) For each job in table A, copy the full text of "About the job".
```
