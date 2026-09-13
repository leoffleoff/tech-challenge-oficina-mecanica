from datetime import datetime
from typing import List, Optional
import uuid

from app.domain.value_objects.status_os import StatusOS

class OrdemServico:
    """
    Aggregate Root que controla as regras de transição de status da Ordem de Serviço.
    """
    def __init__(self, cliente_id: uuid.UUID, veiculo_id: uuid.UUID):
        self.id = uuid.uuid4()
        self.cliente_id = cliente_id
        self.veiculo_id = veiculo_id
        self.status = StatusOS.RECEBIDA
        self.data_criacao = datetime.now()
        self.data_finalizacao: Optional[datetime] = None
        self.valor_total: float = 0.0

    def iniciar_diagnostico(self) -> None:
        if self.status != StatusOS.RECEBIDA:
            raise ValueError(f"Não é possível iniciar diagnóstico a partir do status: {self.status.value}")
        self.status = StatusOS.EM_DIAGNOSTICO

    def enviar_para_aprovacao(self, valor_total_calculado: float) -> None:
        if self.status != StatusOS.EM_DIAGNOSTICO:
            raise ValueError(f"Orçamento só pode ser gerado quando em diagnóstico.")
        if valor_total_calculado <= 0:
            raise ValueError("O valor do orçamento deve ser maior que zero.")
        
        self.valor_total = valor_total_calculado
        self.status = StatusOS.AGUARDANDO_APROVACAO

    def aprovar_orcamento(self) -> None:
        if self.status != StatusOS.AGUARDANDO_APROVACAO:
            raise ValueError(f"Apenas ordens aguardando aprovação podem ser executadas.")
        self.status = StatusOS.EM_EXECUCAO

    def finalizar_execucao(self) -> None:
        if self.status != StatusOS.EM_EXECUCAO:
            raise ValueError(f"Apenas ordens em execução podem ser finalizadas.")
        self.status = StatusOS.FINALIZADA
        self.data_finalizacao = datetime.now()

    def entregar_veiculo(self) -> None:
        if self.status != StatusOS.FINALIZADA:
            raise ValueError(f"O veículo só pode ser entregue se a OS estiver finalizada.")
        self.status = StatusOS.ENTREGUE
        