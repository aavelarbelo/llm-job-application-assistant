# Prompts

The three prompts the system actually runs on, **translated from Portuguese and anonymised**.

| File | Used in | What it does |
|---|---|---|
| [`project-system-prompt.md`](project-system-prompt.md) | Claude project instructions | Posting → fit score → 1-page CV → recruiter message → interview questions |
| [`job-screening-prompt.md`](job-screening-prompt.md) | Claude in Chrome (read-only) | Goes through a LinkedIn results page and shortlists jobs worth applying to |
| [`form-filling-agent-prompt.md`](form-filling-agent-prompt.md) | Claude in Chrome | Fills an application form, with hard stops at login, CV upload and submit |

The n8n workflow has its own screening prompt, built in code; see the `Preparar prompt` node
in [`../n8n/workflow_candidaturas_SANITIZADO.json`](../n8n/workflow_candidaturas_SANITIZADO.json).

## What was changed for publication

- **Personal data** (name, contacts, links): replaced with "Jane Doe" or `[PLACEHOLDERS]`.
- **Institutions, employers and project names:** replaced with fictional ones.
- **Career-specific facts** (degrees, years, grades, skills): replaced with the fictional
  profile in [`../knowledge-base/master-profile.example.md`](../knowledge-base/master-profile.example.md).
- **Forbidden claims:** the real list named specific unproven numbers from old CVs. Those are
  replaced with Jane Doe equivalents, but the categories are the same: unproven percentages,
  group totals presented as individual work, inflated job titles, tools only seen in coursework,
  and empty self-praise.
- **Language:** translated from Portuguese.

Not changed: the flow, the decision rules (score thresholds, discard rules, 60% criterion),
the stop points, the forbidden actions and the output formats.
