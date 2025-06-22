# Em: app/models/schemas.py

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from app.database import Base

# --- MODELOS DE BANCO DE DADOS (SQLAlchemy) ---

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)  # <-- ADICIONE ESTA LINHA
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    lesson_plans = relationship("LessonPlan", back_populates="owner")

class LessonPlan(Base):
    __tablename__ = "lesson_plans"

    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String, index=True)
    grade = Column(String)
    subject = Column(String)
    content = Column(Text)
    
    # A chave estrangeira que aponta para o id da tabela 'users'
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    # A relação inversa, que permite que um LessonPlan saiba quem é seu 'owner'
    owner = relationship("User", back_populates="lesson_plans")

# --- MODELOS DE DADOS DA API (Pydantic) ---

class LessonPlanRequest(BaseModel):
    topic: str
    grade: str
    subject: str

class LessonPlanInList(BaseModel):
    id: int
    topic: str
    grade: str
    subject: str

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    name: str
    password: str

class UserOut(UserBase):
    id: int
    name: str
    is_active: bool

    class Config:
        from_attributes = True