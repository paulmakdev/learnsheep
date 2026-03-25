from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Learnsheep API",
    description="Backend API for Learnsheep educational platform",
    version="1.0.0"
)

app.middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get('/health')
async def health_check():
    return {"status": "healthy", "service": "learnsheep-api"}