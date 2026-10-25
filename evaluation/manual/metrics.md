## Metrics

Rate each generated portfolio on the six metrics below, from 1 to 6. **On every metric, 6 is the best and 1 is the worst.** There's no middle score, so for each one decide whether it leans good (4–6) or bad (1–3).

Open the generated HTML in a browser, check it at desktop and phone width, and keep the resume and the real portfolio open next to it.

| Key | Question |
|---|---|
| `visual_fit` | Does it look like a portfolio someone in this field would have, and is it appealing? |
| `hireability` | Would you hire someone who had this portfolio? |
| `resume_fidelity` | How well does it capture the content of the resume? |
| `portfolio_fidelity` | How well does it capture the content of their real portfolio? |
| `natural_language` | Is it written in natural, conversational sentences, not resume-style bullet points? |
| `factual_accuracy` | Is everything in it true to the resume, with no made-up facts? |

### Scoring guide

**visual_fit**
- 6: Looks professionally designed and the style clearly suits their field. Works on desktop and mobile.
- 3–4: Clean and usable but generic, or the style doesn't quite match the field.
- 1: Broken layout, unreadable, or clearly the wrong style for the field.

**hireability**
- 6: It would make a strong first impression on a recruiter in this field.
- 3–4: It doesn't hurt the candidate, but it wouldn't make them stand out.
- 1: It would make you less likely to hire them.

**resume_fidelity**
- 6: Every section and important detail from the resume is there (experience, projects, education, skills, awards, etc.).
- 3–4: The main sections are there, but some details or a minor section are missing.
- 1: Large parts of the resume are missing.

**portfolio_fidelity**
- 6: It covers the same content as their real portfolio.
- 3–4: It overlaps with the real portfolio on the main points but misses things or adds others.
- 1: It has little in common with the real portfolio.
- Content that's only on the real portfolio and not on the resume will lower this score. That's expected, so don't take points off other metrics for it.

**natural_language**
- 6: Reads like the person wrote it themselves: full, conversational sentences throughout.
- 3–4: A mix of sentences and resume-style fragments or bullet lists.
- 1: Basically the resume copied over: bullet points, fragments, and lists of metrics.

**factual_accuracy**
- 6: No made-up facts. Everything can be traced back to the resume.
- 3–4: One or two small invented or exaggerated details (e.g. a skill or tool not on the resume).
- 1: Major made-up content, such as a fake job, project, degree, or number.
- Placeholders like `[INSERT LINKEDIN LINK HERE]` are what the prompt asks for, so they are **not** hallucinations. A made-up URL is.
- List every made-up fact you find in NOTES.

### File format

Save one file per sample as `[pair_number]_metrics.txt` in this folder. Copy this template (see `0001_metrics_example.txt`):

```
PAIR: 0001
RATER: <your name>

visual_fit (1-6):
hireability (1-6):
resume_fidelity (1-6):
portfolio_fidelity (1-6):
natural_language (1-6):
factual_accuracy (1-6):

NOTES:
```
