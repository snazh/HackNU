import random
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from src.models.user import User, UserRole
from src.models.resume import Resume
from src.models.vacancy import Vacancy, VacancyApplication, EducationLevel, ApplicationStatus, EmploymentForm
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from src.config import settings
from contextlib import asynccontextmanager
fake = Faker()

# --- Async DB session ---
engine = create_async_engine(settings.db.async_database_url)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

@asynccontextmanager
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

# --- Seed constants ---
NUM_USERS = 20
NUM_VACANCIES = 10
NUM_APPLICATIONS = 30

IT_JOBS = [
    "Software Engineer",
    "Backend Developer",
    "Frontend Developer",
    "Data Scientist",
    "DevOps Engineer"
]

IT_SKILLS = ["Python", "JavaScript", "SQL", "Docker", "Kubernetes", "React", "Node.js", "Git"]
IT_LANGUAGES = ["English", "Spanish", "German", "French"]
VALID_EMPLOYMENT_FORMS = [EmploymentForm.FULL_TIME, EmploymentForm.PART_TIME, EmploymentForm.REMOTE]

# --- Seed function ---
async def seed_all():
    async with get_async_session() as session:
        # Очистка таблиц
        await session.execute(text("DELETE FROM vacancy_applications;"))
        await session.execute(text("DELETE FROM vacancies;"))
        await session.execute(text("DELETE FROM resumes;"))
        await session.execute(text("DELETE FROM users WHERE id <> 1;"))
        await session.commit()

        # Создаем пользователей и резюме
        users = []
        for _ in range(NUM_USERS):
            role = random.choice(list(UserRole))
            user = User(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.unique.email(),
                password=fake.password(),
                role=role
            )
            session.add(user)
            await session.flush()
            users.append(user)

            if role != UserRole.hr:
                experience_list = []
                for job in random.sample(IT_JOBS, 2):
                    experience_list.append({
                        "company": fake.company(),
                        "position": job,
                        "years": random.randint(1, 10)
                    })

                skills_list = random.sample(IT_SKILLS, 5)
                languages_list = random.sample(IT_LANGUAGES, 2)
                resume = Resume(
                    user_id=user.id,
                    title=random.choice(IT_JOBS),
                    summary=fake.text(max_nb_chars=200),
                    skills=skills_list,
                    experience=experience_list,
                    education=random.choice(list(EducationLevel)),
                    languages=languages_list,
                    location=fake.city(),
                    salary_expectation=f"{random.randint(3000, 15000)} USD",
                    employment_form=random.choice(VALID_EMPLOYMENT_FORMS)
                )
                session.add(resume)

        await session.flush()

        # Создаем вакансии
        hr_users = [u for u in users if u.role == UserRole.hr]
        vacancies = []
        for _ in range(NUM_VACANCIES):
            hr = random.choice(hr_users)
            vacancy = Vacancy(
                title=random.choice(IT_JOBS),
                description=fake.text(max_nb_chars=300),
                company=fake.company(),
                location=fake.city(),
                salary=f"{random.randint(3000, 15000)} USD",
                hr_id=hr.id,
                skills=random.sample(IT_SKILLS, 3),
                education=random.choice(list(EducationLevel)),
                employment_form=random.choice(VALID_EMPLOYMENT_FORMS)
            )
            session.add(vacancy)
            await session.flush()
            vacancies.append(vacancy)

        # Создаем отклики
        normal_users = [u for u in users if u.role != UserRole.hr]
        for _ in range(NUM_APPLICATIONS):
            user = random.choice(normal_users)
            vacancy = random.choice(vacancies)
            application = VacancyApplication(
                user_id=user.id,
                vacancy_id=vacancy.id,
                message=fake.text(max_nb_chars=200),
                status=random.choice(list(ApplicationStatus))
            )
            session.add(application)

        await session.commit()
        print("Seed completed!")

if __name__ == "__main__":
    import asyncio
    asyncio.run(seed_all())