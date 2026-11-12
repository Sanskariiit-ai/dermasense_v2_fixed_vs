from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes.auth import router as auth_router
from api.routes.chat import router as chat_router
from api.routes.patient import router as patient_router
from api.routes.reports import router as report_router
from api.routes.voice import router as voice_router
from api.routes.ws import router as ws_router
from config.settings import jwt_secret, settings
from db.mongo import ensure_indexes


@asynccontextmanager
async def lifespan(app: FastAPI):
    jwt_secret()  # fail fast in production if the secret is missing
    await ensure_indexes()
    yield


app = FastAPI(title="DermaSense AI", version="2.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_list,  # explicit origins: "*" is not allowed together with credentials
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

for r in (auth_router, patient_router, chat_router, report_router, voice_router, ws_router):
    app.include_router(r)


@app.get("/")
def health_check():
    return {"status": "running", "version": app.version}
