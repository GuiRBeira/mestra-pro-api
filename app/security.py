# Em: app/security.py
from passlib.context import CryptContext

# Define o algoritmo de hashing que vamos usar (bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se uma senha em texto puro corresponde a um hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Cria o hash de uma senha em texto puro."""
    return pwd_context.hash(password)