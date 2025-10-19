import json
from openai import OpenAI
from src.models.resume import Resume
from src.models.vacancy import Vacancy
from typing import Dict
from src.config import settings


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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"
)

def ask_questions(resume: Resume, vacancy: Vacancy) -> list[str]:
    """
    Generates clarifying questions to ask the candidate
    based on mismatches between their resume and the vacancy.
    """
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
You are a recruitment assistant.
Compare the candidate’s resume and the vacancy details.
Find the main mismatches and generate clarifying questions
that the employer can ask the candidate to resolve uncertainty.

Rules:
- Focus only on missing, unclear, or mismatched information.
- Keep questions short and professional.
- Return ONLY JSON with an array of strings like this:

{{
    "questions": [
        "Do you have experience with Node.js?",
        "Are you open to relocating to New Diana?",
        "Would you consider a part-time position?"
    ]
}}

Candidate resume:
{resume_text}

Vacancy:
{vacancy_text}
"""

    completion = client.chat.completions.create(
        model="deepseek/deepseek-r1-0528-qwen3-8b:free",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    try:
        content = completion.choices[0].message.content
        cleaned = content.replace("```json", "").replace("```", "").strip()
        data = json.loads(cleaned)
        return data.get("questions", [])
    except Exception:
        return ["Could not generate clarifying questions. Please try again."]
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

    completion = client.chat.completions.create(

        extra_body={},
        model="deepseek/deepseek-r1-0528-qwen3-8b:free",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"{prompt}"
                    }
                ]
            }
        ]
    )
    return completion.choices[0].message.content
