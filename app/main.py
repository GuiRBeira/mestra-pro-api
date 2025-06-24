# Em: app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Importa os roteadores existentes e o novo roteador do beamer
from app.api import lesson_plan_router, auth_router, beamer_router

app = FastAPI(title="MestraPro API")

origins = [
    "http://localhost:5173",
    "127.0.0.1:5173",
    "https://mestrapro.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui as rotas de autenticação
app.include_router(auth_router.router, prefix="/auth", tags=["Autenticação"])
# Inclui as rotas de planos de aula
app.include_router(lesson_plan_router.router, prefix="/api/v1", tags=["Planos de Aula"])
# INCLUI AS NOVAS ROTAS PARA GERAÇÃO DE SLIDES BEAMER
app.include_router(beamer_router.router, prefix="/api/v1/beamer", tags=["Slides Beamer"])