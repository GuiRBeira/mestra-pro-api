# Em: app/api/auth_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models import schemas
from app.database import get_db
from app.security import get_password_hash # Importa nossa função de hash
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.security import verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from app.security import SECRET_KEY, ALGORITHM, jwt

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

    new_user = schemas.User(
        email=user.email, # Adiciona o e-mail do usuário
        name=user.name,   # Adiciona o nome do usuário
        hashed_password=hashed_password # Usa a função de hash para a senha
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/login")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Busca o usuário pelo e-mail (que no OAuth2PasswordRequestForm vem no campo 'username')
    user = db.query(schemas.User).filter(schemas.User.email == form_data.username).first()

    # Verifica se o usuário existe e se a senha está correta
    if not user or not verify_password(form_data.password, user.hashed_password): # type: ignore
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Gera o token de acesso
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) #type: ignore
        email: str = payload.get("sub") #type: ignore
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(schemas.User).filter(schemas.User.email == email).first()
    if user is None:
        raise credentials_exception
    return user