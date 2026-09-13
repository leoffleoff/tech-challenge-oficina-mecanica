import uuid
import pytest
from app.domain.aggregates.ordem_servico import OrdemServico
from app.domain.value_objects.status_os import StatusOS


@pytest.fixture
def os_valida() -> OrdemServico:
    """Fixture que fornece uma instância padrão de OrdemServico recém-criada."""
    cliente_id = uuid.uuid4()
    veiculo_id = uuid.uuid4()
    return OrdemServico(cliente_id=cliente_id, veiculo_id=veiculo_id)


def test_criar_ordem_servico_com_status_recebida(os_valida: OrdemServico):
    """Garante que toda nova OS nasce no status RECEBIDA."""
    assert os_valida.status == StatusOS.RECEBIDA
    assert os_valida.valor_total == 0.0
    assert os_valida.data_finalizacao is None


def test_fluxo_completo_com_sucesso(os_valida: OrdemServico):
    """Testa a transição completa do ciclo de vida da OS."""
    # 1. Iniciar diagnóstico
    os_valida.iniciar_diagnostico()
    assert os_valida.status == StatusOS.EM_DIAGNOSTICO

    # 2. Enviar para aprovação com orçamento
    os_valida.enviar_para_aprovacao(valor_total_calculado=450.0)
    assert os_valida.status == StatusOS.AGUARDANDO_APROVACAO
    assert os_valida.valor_total == 450.0

    # 3. Aprovar orçamento
    os_valida.aprovar_orcamento()
    assert os_valida.status == StatusOS.EM_EXECUCAO

    # 4. Finalizar execução
    os_valida.finalizar_execucao()
    assert os_valida.status == StatusOS.FINALIZADA
    assert os_valida.data_finalizacao is not None

    # 5. Entregar veículo
    os_valida.entregar_veiculo()
    assert os_valida.status == StatusOS.ENTREGUE


def test_erro_transicao_invalida_diagnostico_sem_recebida(os_valida: OrdemServico):
    """Valida que não é possível iniciar diagnóstico se a OS não estiver RECEBIDA."""
    os_valida.iniciar_diagnostico()  # Status agora é EM_DIAGNOSTICO

    with pytest.raises(ValueError, match="Não é possível iniciar diagnóstico"):
        os_valida.iniciar_diagnostico()


def test_erro_orcamento_com_valor_invalido(os_valida: OrdemServico):
    """Garante que um orçamento com valor menor ou igual a zero é rejeitado."""
    os_valida.iniciar_diagnostico()

    with pytest.raises(ValueError, match="O valor do orçamento deve ser maior que zero."):
        os_valida.enviar_para_aprovacao(valor_total_calculado=0.0)


def test_erro_entregar_veiculo_sem_finalizar(os_valida: OrdemServico):
    """Garante que não é possível entregar o veículo diretamente sem finalizar a OS."""
    with pytest.raises(ValueError, match="O veículo só pode ser entregue se a OS estiver finalizada."):
        os_valida.entregar_veiculo()
        