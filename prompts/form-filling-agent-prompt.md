# Form-filling agent prompt (browser agent with hard stops)

**Used with:** Claude in Chrome, on the tab of a specific job posting. The real example was a
corporate applicant-tracking portal.

**Input:** an open job page. **Output:** a filled-in form that has **not** been submitted, plus
a summary of every field for human review.

> Translated from Portuguese. Contact details are placeholders; education and dates are my
> own. The four rules and the consent rule are unchanged.

Design notes:
- **Hard stop points, not "be careful".** The agent stops at login/password, at CV upload and
  before the final submit. Credentials and files never go through the agent.
- **Closed data set.** If a field asks for anything not in the list, the agent stops and asks
  instead of improvising. This is the same single-source-of-truth rule as the CV generator.
- **Explicit answers for tricky questions.** For example, how to answer "Do you have a
  master's?" when a programme was started but not completed (see `docs/lessons-learned.md`).
- **Privacy by default** for consent checkboxes: only the mandatory ones.

---

```text
You are on the tab of the job [JOB] ([SITE]). Help me fill in the application. Rules:

1. Click "Apply now". If an account or login is required, STOP and ask me to enter the email
   and password myself.
2. Fill in the fields ONLY with the data below. If a field asks for something that isn't here,
   STOP and ask me. Don't make anything up.
3. At the CV upload, STOP and ask me to upload the file myself.
4. NEVER click the final submit button. When the form is complete, show me a summary of
   everything you filled in and wait for my confirmation.

DATA:
- Name / Email / Phone / Location: [PERSONAL DATA]
- Work authorisation in Portugal: Yes, no visa needed
- LinkedIn / GitHub: [LINKS]
- Education: Postgraduate Programme in Big Data & Decision Making, ISEP
  (Nov 2025 to Jun 2026, average 15/20); BSc in Control & Automation Engineering (2014 to 2019);
  if asked about a master's: MSc in Computational Mechanics, FEUP, NOT completed
- Languages: Portuguese (native); English (B2)
- Most relevant experience: [EMPLOYERS AND DATES]
- Availability: immediate · How did you hear about the job: LinkedIn
- Salary expectation (if asked, as text): "I am open to an offer aligned with the company's
  policy for the programme."
- GDPR consents: you may tick the mandatory ones for the recruitment process; DO NOT tick
  marketing/newsletter ones without asking me.
```
