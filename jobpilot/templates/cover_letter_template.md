{{ profile.name }}  
{{ profile.email }} | {{ profile.phone }}

Dear Hiring Manager,

I am writing to express my interest in the **{{ job.title }}** position{% if job.company %} at **{{ job.company }}**{% endif %}.

My background is focused on {{ profile.summary }} I have practical experience with {{ profile.skills[:5] | join(', ') }}, and I am especially interested in applying AI tools to improve job matching, document generation and evaluation workflows.

Based on the JobPilot fit analysis, the current matching score is **{{ fit.score }}%**. The most relevant overlapping skills are: {{ fit.matched_skills | join(', ') }}.

To further match this role, I will continue improving: {{ fit.missing_skills[:5] | join(', ') }}.

Thank you for your time and consideration. I would welcome the opportunity to discuss how my AI evaluation, Prompt Engineering and Python tooling experience can contribute to your team.

Sincerely,

{{ profile.name }}
