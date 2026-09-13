from typing import Optional, List
import uuid
from sqlalchemy.orm import Session

from app.domain.aggregates.ordem_servico import OrdemServico
from app.domain.repositories.os_repository import OrdemServicoRepositoryInterface
from app.infrastructure.database.models import OrdemServicoModel


class OrdemServicoRepositoryImpl(OrdemServicoRepositoryInterface):
    """
    Implementação concreta do repositório utilizando SQLAlchemy e PostgreSQL.
    """
    def __init__(self, session: Session):
        self.session = session

    def salvar(self, ordem_servico: OrdemServico) -> None:
        # Verifica se a OS já existe no banco
        model = self.session.query(OrdemServicoModel).filter_by(id=ordem_servico.id).first()

        if not model:
            # Cria novo registro
            model = OrdemServicoModel(
                id=ordem_servico.id,
                cliente_id=ordem_servico.cliente_id,
                veiculo_id=ordem_servico.veiculo_id,
                status=ordem_servico.status,
                valor_total=ordem_servico.valor_total,
                data_criacao=ordem_servico.data_criacao,
                data_finalizacao=ordem_servico.data_finalizacao
            )
            self.session.add(model)
        else:
            # Atualiza o estado da OS existente
            model.status = ordem_servico.status
            model.valor_total = ordem_servico.valor_total
            model.data_finalizacao = ordem_servico.data_finalizacao

        self.session.commit()

    def buscar_por_id(self, os_id: uuid.UUID) -> Optional[OrdemServico]:
        model = self.session.query(OrdemServicoModel).filter_by(id=os_id).first()
        if not model:
            return None
        return self._to_domain(model)

    def listar_todas(self) -> List[OrdemServico]:
        models = self.session.query(OrdemServicoModel).all()
        return [self._to_domain(m) for m in models]

    def _to_domain(self, model: OrdemServicoModel) -> OrdemServico:
        """Converte um registro do banco (Model) de volta para o Agregado do Domínio."""
        os = OrdemServico(cliente_id=model.cliente_id, veiculo_id=model.veiculo_id)
        os.id = model.id
        os.status = model.status
        os.valor_total = model.valor_total
        os.data_criacao = model.data_criacao
        os.data_finalizacao = model.data_finalizacao
        return os