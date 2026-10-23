## Prompt
Here is the prompt we gave to Claude to generate portfolios from our input:

You are given a person's resume. Create a personal portfolio website for them, with a visual style that suits their field and personality as suggested by the resume.

Output:
- A single, self-contained HTML file, with all CSS in a <style> tag and all JS in a <script> tag.
- Do not use external images or files that might not exist. Use CSS shapes, gradients, or initials for visuals. Web fonts and icon libraries are fine to skip.
- The site should be responsive and work on desktop and mobile.

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