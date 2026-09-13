from abc import ABC, abstractmethod
from typing import Optional, List
import uuid

from app.domain.aggregates.ordem_servico import OrdemServico


class OrdemServicoRepositoryInterface(ABC):
    """
    Interface/Contrato para persistência do Agregado OrdemServico.
    A camada de Infraestrutura ficará responsável por implementar estes métodos.
    """

    @abstractmethod
    def salvar(self, ordem_servico: OrdemServico) -> None:
        """Persiste ou atualiza uma Ordem de Serviço no banco de dados."""
        pass

    @abstractmethod
    def buscar_por_id(self, os_id: uuid.UUID) -> Optional[OrdemServico]:
        """Busca uma Ordem de Serviço pelo seu ID único."""
        pass

    @abstractmethod
    def listar_todas(s) -> List[OrdemServico]:
        """Lista todas as Ordens de Serviço cadastradas."""
        pass
    
