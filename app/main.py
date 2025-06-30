from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import lesson_plan_router, auth_router

app = FastAPI(title="MestraPro API")

origins = ["http://localhost:5173",
           "127.0.0.1:5173",
           "https://mestrapro.vercel.app",
           ]

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])

# Inclui todas as rotas do nosso arquivo de rotas na aplicação principal
app.include_router(auth_router.router, prefix="/auth", tags=["Autenticação"])
app.include_router(lesson_plan_router.router, prefix="/api/v1", tags=["Planos de Aula"])