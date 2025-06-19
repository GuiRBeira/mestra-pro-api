# Em: app/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Carrega as variáveis de ambiente (onde está nossa DATABASE_URL)
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("A variável de ambiente DATABASE_URL não foi encontrada.")

# O "motor" que o SQLAlchemy usa para se comunicar com o banco
engine = create_engine(DATABASE_URL)

# Cria uma "fábrica" de sessões de banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Uma classe base que nossos modelos de tabela irão herdar
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()