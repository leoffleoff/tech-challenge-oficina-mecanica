from sqlalchemy import Column, String, Float, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

from app.infrastructure.database.connection import Base
from app.domain.value_objects.status_os import StatusOS


class OrdemServicoModel(Base):
    """
    Modelo ORM que representa a tabela 'ordens_servico' no PostgreSQL.
    """
    __tablename__ = "ordens_servico"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cliente_id = Column(UUID(as_uuid=True), nullable=False)
    veiculo_id = Column(UUID(as_uuid=True), nullable=False)
    status = Column(SQLEnum(StatusOS), nullable=False, default=StatusOS.RECEBIDA)
    valor_total = Column(Float, nullable=False, default=0.0)
    data_criacao = Column(DateTime, nullable=False, default=datetime.now)
    data_finalizacao = Column(DateTime, nullable=True)
    