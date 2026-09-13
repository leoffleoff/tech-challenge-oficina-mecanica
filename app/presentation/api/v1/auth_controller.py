from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from app.infrastructure.security.jwt_auth import (
    verificar_senha,
    gerar_hash_senha,
    criar_token_acesso,
)

router = APIRouter(prefix="/api/v1/auth", tags=["Autenticação"])

# Usuário administrador padrão para testes do MVP
# Em produção, este usuário estaria armazenado e buscado na tabela de usuários do banco
ADMIN_USUARIO_DB = {
    "username": "admin@oficina.com",
    "password_hash": gerar_hash_senha("admin123")  # Senha padrão de teste
}


class TokenDTO(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/login", response_model=TokenDTO)
def login_para_obter_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Endpoint administrativo para autenticação e geração do Bearer JWT Token.
    """
    if form_data.username != ADMIN_USUARIO_DB["username"] or not verificar_senha(
        form_data.password, ADMIN_USUARIO_DB["password_hash"]
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = criar_token_acesso(dados={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}
