from datetime import datetime, timedelta, timezone
from typing import Optional
import os

from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# Configurações de segurança via variáveis de ambiente
SECRET_KEY = os.getenv("JWT_SECRET", "sua_chave_secreta_para_desenvolvimento_12345")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Substituído para pbkdf2_sha256 para evitar conflitos de versão do bcrypt
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# Esquema OAuth2 que lê o token do Header "Authorization: Bearer <TOKEN>"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    """Verifica se a senha em texto plano confere com o hash armazenado."""
    return pwd_context.verify(senha_plana, senha_hash)


def gerar_hash_senha(senha: str) -> str:
    """Gera o hash seguro da senha."""
    return pwd_context.hash(senha)


def criar_token_acesso(dados: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Gera um novo Token JWT assinado."""
    to_encode = dados.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def obter_usuario_atual(token: str = Depends(oauth2_scheme)) -> str:
    """
    Dependência FastAPI que valida o token JWT presente na requisição.
    Se o token for inválido ou expirado, lança exceção HTTP 401 Unauthorized.
    """
    excecao_credenciais = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais de acesso.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise excecao_credenciais
        return username
    except JWTError:
        raise excecao_credenciais