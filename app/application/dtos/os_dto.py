from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid


class CriarOSInputDTO(BaseModel):
    """DTO de entrada para abertura de uma nova Ordem de Serviço."""
    cpf_cnpj_cliente: str = Field(..., description="CPF ou CNPJ do cliente", example="123.456.789-01")
    placa_veiculo: str = Field(..., description="Placa do veículo", example="ABC-1234")
    marca_veiculo: str = Field(..., description="Marca do veículo", example="Volkswagen")
    modelo_veiculo: str = Field(..., description="Modelo do veículo", example="Gol")
    ano_veiculo: int = Field(..., description="Ano de fabricação", example=2020)


class AprovarOrcamentoInputDTO(BaseModel):
    """DTO de entrada para aprovação do orçamento pelo cliente."""
    os_id: uuid.UUID = Field(..., description="ID da Ordem de Serviço")


class OSOutputDTO(BaseModel):
    """DTO de saída com as informações consolidadas da Ordem de Serviço."""
    id: uuid.UUID
    cliente_id: uuid.UUID
    veiculo_id: uuid.UUID
    status: str
    valor_total: float
    data_criacao: datetime
    data_finalizacao: Optional[datetime] = None

    class Config:
        from_attributes = True
        