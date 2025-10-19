import openai
from src.models.resume import Resume
from src.models.vacancy import Vacancy
from typing import Dict
from src.config import settings
openai.api_key = settings.external_api.OPENAI_API_KEY


async def generate_follow_up_questions(resume: Resume, vacancy: Vacancy) -> list[str]:
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
You are an AI assistant. Your task is to generate follow-up questions for a candidate.
Compare the candidate's resume with the vacancy requirements.
- Identify discrepancies in: city, experience, position, education, languages, salary, employment form.
- Generate **up to 3 concise, human-like, friendly questions** to clarify mismatches.
- If there are fewer than 3 discrepancies, fill the rest with "No further questions".
- Output strictly as a JSON array of 3 strings.

Candidate resume:
{resume_text}

Vacancy:
{vacancy_text}
"""

    response = await openai.ChatCompletion.acreate(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    questions = json.loads(response.choices[0].message["content"])

    # Ensure exactly 3 questions
    while len(questions) < 3:
        questions.append("No further questions")
    return questions[:3]

# 2️⃣ Analyze chat history and give final decision
async def analyze_final_decision(resume: Resume, vacancy: Vacancy, chat_history: list[Dict[str, str]]) -> Dict:
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

    chat_text = "\n".join([f"Q: {q['question']}\nA: {q['answer']}" for q in chat_history])

    prompt = f"""
You are an AI assistant evaluating a candidate for a job.
Candidate resume:
{resume_text}

Vacancy:
{vacancy_text}

Candidate responses to follow-up questions:
{chat_text}

Task:
1. Evaluate how well the candidate fits the vacancy.
2. Consider mismatches from resume and responses.
3. Provide relevance percentage (0-100).
4. Give a short summary for the employer explaining reasoning.
5. Output as JSON:
{{
    "final_relevance_percentage": int,
    "final_summary_for_employer": str
}}
"""

    response = await openai.ChatCompletion.acreate(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    import json
    return json.loads(response.choices[0].message["content"])