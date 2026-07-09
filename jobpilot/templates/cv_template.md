# {{ profile.name }}

**Email:** {{ profile.email }}  
**Phone:** {{ profile.phone }}

## Summary

{{ profile.summary }}

{% if job and fit %}
## Target Role Match: {{ job.title }}

**Fit score:** {{ fit.score }}%

**Matched skills:** {{ fit.matched_skills | join(', ') }}

{% endif %}

## Skills

{% for skill in profile.skills %}
- {{ skill }}
{% endfor %}

## Experience

{% for exp in profile.experience %}
### {{ exp.role }}｜{{ exp.company }}（{{ exp.start_year }} - {{ exp.end_year or 'Present' }}）

{{ exp.description }}

{% endfor %}

## Education

{% for edu in profile.education %}
- **{{ edu.institution }}**｜{{ edu.degree }}｜{{ edu.field }}（{{ edu.start_year }} - {{ edu.end_year or 'Present' }}）
{% endfor %}
