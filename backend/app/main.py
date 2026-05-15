from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.auth import router as auth_router
from app.api.question import router as question_router
from app.api.me import router as me_router
from app.api.stat import router as stat_router
import logging
from app.core.config import settings

logging.basicConfig(level=logging.DEBUG)

app = FastAPI(
    title="Learnsheep API",
    description="Backend API for Learnsheep educational platform",
    version="1.0.0",
)

app.include_router(auth_router, prefix="/api")
app.include_router(question_router, prefix="/api")
app.include_router(me_router, prefix="/api")
app.include_router(stat_router, prefix="/api")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://dev.learnsheep.com",
        "https://learnsheep.com",
        *(["https://localhost:3000"] if settings.environment != "production" else []),
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "learnsheep-api"}
