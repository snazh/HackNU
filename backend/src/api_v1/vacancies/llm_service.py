import json
from openai import OpenAI
from src.models.resume import Resume
from src.models.vacancy import Vacancy
from typing import Dict
from src.config import settings


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=settings.external_api.OPENAI_API_KEY
)


def analyze_resume(resume: Resume, vacancy: Vacancy) -> Dict:
    resume_text = f"""
Title: {resume.title}
Summary: {resume.summary}
Experience: {resume.experience} years
Skills: {', '.join(resume.skills or [])}
Education: {resume.education.value if resume.education else 'N/A'}
Languages: {', '.join(resume.languages or [])}
Location: {resume.location}
Salary Expectation: {resume.salary_expectation}
Employment Form: {resume.employment_form.value if resume.employment_form else 'N/A'}
"""

    vacancy_text = f"""
Title: {vacancy.title}
Description: {vacancy.description}
Skills: {', '.join(vacancy.skills or [])}
Education: {vacancy.education.value if vacancy.education else 'N/A'}
Location: {vacancy.location}
Salary: {vacancy.salary}
Employment Form: {vacancy.employment_form.value if vacancy.employment_form else 'N/A'}
"""

    prompt = f"""
You are an AI assistant evaluating a candidate for a job.
Compare the candidate's resume with the vacancy requirements.
Task:
1. Evaluate how well the candidate fits the vacancy.
2. Consider mismatches only from the resume.
3. Provide relevance percentage (0–100).
4. Give a short summary for the employer explaining reasoning.
5. Output strictly as JSON:
{{
    "final_relevance_percentage": int,
    "final_summary_for_employer": str
}}

Candidate resume:
{resume_text}

Vacancy:
{vacancy_text}
"""

    response = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": "https://your-site.com",
            "X-Title": "VacancyAnalyzer",
        },
        model="openai/gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    raw_content = response.choices[0].message.content
    return json.loads(raw_content)
