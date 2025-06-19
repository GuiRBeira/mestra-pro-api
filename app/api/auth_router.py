# Em: app/api/auth_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models import schemas
from app.database import get_db
from app.security import get_password_hash # Importa nossa função de hash

router = APIRouter()

@router.post("/register", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Verifica se o usuário já existe no banco de dados
    db_user = db.query(schemas.User).filter(schemas.User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E-mail já registrado"
        )

    # Cria o hash da senha recebida do front-end
    hashed_password = get_password_hash(user.password)

    # Cria um novo objeto de usuário para o banco de dados
    new_user = schemas.User(email=user.email, hashed_password=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user