from contextlib import asynccontextmanager
from typing import Union

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from src.api_v1.auth.router import router as auth_router
from src.api_v1.users.router import router as user_router
from src.api_v1.vacancies.router import router as vacancy_router
from src.api_v1.common.errors import BaseAppException
from src.api_v1.resume.router import router as resume_router
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("✅ Запуск приложения")
    yield
    print("🛑 Завершение приложения")


app = FastAPI(title="HackNU Backend",lifespan=lifespan)
app.include_router(auth_router, prefix="/api")
app.include_router(user_router, prefix="/api")
app.include_router(vacancy_router, prefix="/api")
app.include_router(resume_router, prefix="/api")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # можно ограничить ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "FastAPI is running!"}


@app.exception_handler(BaseAppException)
async def base_app_exception_handler(request: Request, exc: BaseAppException) -> Union[JSONResponse, Response]:
    return JSONResponse(
        status_code=exc.status_code,
        content={"status": "Failure", "msg": exc.detail},
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> Union[JSONResponse, Response]:
    return JSONResponse(
        status_code=500,
        content={"status": "Failure", "msg": f"Internal Server Error: {exc}"},
    )
