from fastapi import FastAPI, Depends, HTTPException, status
from typing import List

from app.infrastructure.database.connection import Base, engine, get_db
from app.infrastructure.repositories.os_repository_impl import OrdemServicoRepositoryImpl
from app.application.use_cases.criar_os_use_case import CriarOrdemServicoUseCase
from app.application.dtos.os_dto import CriarOSInputDTO, OSOutputDTO
from app.infrastructure.security.jwt_auth import obter_usuario_atual
from app.presentation.api.v1.auth_controller import router as auth_router

# Cria tabelas no banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema de Gestão de Oficina Mecânica (Tech Challenge MVP)",
    description="API RESTful para gestão de Ordens de Serviço, Clientes e Insumos aplicando DDD.",
    version="1.0.0"
)

# Inclui o módulo de autenticação JWT
app.include_router(auth_router)


@app.get("/", tags=["Healthcheck"])
def healthcheck():
    return {"status": "ok", "mensagem": "API da Oficina Mecânica rodando com sucesso!"}


@app.post(
    "/api/v1/ordens-servico",
    response_model=OSOutputDTO,
    status_code=status.HTTP_201_CREATED,
    tags=["Ordens de Serviço"]
)
def criar_ordem_servico(payload: CriarOSInputDTO, db=Depends(get_db)):
    """
    [Pública / Cliente] Abertura de uma nova Ordem de Serviço (OS).
    """
    try:
        repo = OrdemServicoRepositoryImpl(db)
        use_case = CriarOrdemServicoUseCase(os_repository=repo)
        return use_case.executar(payload)
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))


@app.get(
    "/api/v1/admin/ordens-servico",
    response_model=List[OSOutputDTO],
    tags=["Administrativo (Protegido por JWT)"]
)
def listar_ordens_servico_admin(
    db=Depends(get_db),
    usuario_atual: str = Depends(obter_usuario_atual)
):
    """
    [Administrativa / Protegida] Lista todas as OSs. 
    Exige cabeçalho de autorização: Bearer <TOKEN_JWT>.
    """
    repo = OrdemServicoRepositoryImpl(db)
    ordens = repo.listar_todas()
    return [
        OSOutputDTO(
            id=os.id,
            cliente_id=os.cliente_id,
            veiculo_id=os.veiculo_id,
            status=os.status.value,
            valor_total=os.valor_total,
            data_criacao=os.data_criacao,
            data_finalizacao=os.data_finalizacao
        )
        for os in ordens
    ]
