## Prompt
Here is the prompt we give to Claude to generate portfolios from our input. Copy everything inside the box exactly as written.

```
You are given a person's resume. Create a personal portfolio website for them, with a visual style that suits their field and personality as suggested by the resume.

Output:
- A single, self-contained HTML file, with all CSS in a <style> tag and all JS in a <script> tag.
- Do not use external images or files that might not exist. Use CSS shapes, gradients, or initials for visuals. Web fonts and icon libraries are optional; the page must still look right without them.
- The site should be responsive and work on desktop and mobile.
- Respond with only the complete HTML file, from <!DOCTYPE html> to </html>.

Content:
- Include their experience, projects, education, skills, and any other sections present in the resume (certifications, awards, etc.).
- Include a short "about me" summary written only from information in the resume.
- If the resume has no content for a section, leave that section out.

Tone:
- Casual but professional. Write in complete, conversational sentences that feel inviting, not like resume bullet points.
- Real numbers and achievements from the resume may be worked into sentences naturally.

Accuracy:
- Use only information from the resume. Do not invent facts, experiences, projects, skills, or metrics.
- For any link you can't fill in (LinkedIn, GitHub, project demos, etc.), write a visible placeholder in square brackets, like [INSERT LINKEDIN LINK HERE], and don't make up URLs.
```

## How to run it

Everyone has to generate the same way, or differences between portfolios could come from the setup instead of the resume.

**Setup (same for everyone):**
- Model: Claude Opus 5.5 on claude.ai
- Extended thinking: off
- In claude.ai settings, turn off memory and clear any personal preferences / custom instructions, so nothing about you leaks into the output. Don't run it inside a Project.

**For each resume:**
1. Start a **new chat**.
2. Attach the resume PDF from `data/resumes/<id>.pdf` (the numbered file, so the name doesn't give anything away).
3. Paste the prompt above and send it. Don't add anything else.
4. Use the **first** response. Don't regenerate it or ask for changes, even if it's bad. That's what we're measuring.
   - If the response gets cut off before `</html>`, send `continue` once and join the two parts. Write this down in the NOTES of the manual evaluation.
5. Copy the HTML code (from the artifact's code view if Claude made one) and save it as `output/html/<id>_output.html`.
6. Open the file in a browser to check that it was saved completely before you rate it.

Output files should be stored as:

[pair_number]_output.html
