import pytest
from typing import List, Optional
import uuid

from app.domain.aggregates.ordem_servico import OrdemServico
from app.domain.repositories.os_repository import OrdemServicoRepositoryInterface
from app.application.use_cases.criar_os_use_case import CriarOrdemServicoUseCase
from app.application.dtos.os_dto import CriarOSInputDTO


class FakeOSRepository(OrdemServicoRepositoryInterface):
    """Implementação em memória da interface para uso exclusivo em testes."""
    def __init__(self):
        self._ordens: List[OrdemServico] = []

    def salvar(self, ordem_servico: OrdemServico) -> None:
        self._ordens.append(ordem_servico)

    def buscar_por_id(self, os_id: uuid.UUID) -> Optional[OrdemServico]:
        return next((os for os in self._ordens if os.id == os_id), None)

    def listar_todas(self) -> List[OrdemServico]:
        return self._ordens


def test_criar_ordem_servico_com_sucesso():
    fake_repo = FakeOSRepository()
    use_case = CriarOrdemServicoUseCase(os_repository=fake_repo)

    input_dto = CriarOSInputDTO(
        cpf_cnpj_cliente="123.456.789-01",
        placa_veiculo="ABC-1234",
        marca_veiculo="Toyota",
        modelo_veiculo="Corolla",
        ano_veiculo=2022
    )

    output = use_case.executar(input_dto)

    assert output.id is not None
    assert output.status == "Recebida"
    assert output.valor_total == 0.0
    assert len(fake_repo.listar_todas()) == 1


def test_erro_ao_criar_os_com_cpf_invalido():
    fake_repo = FakeOSRepository()
    use_case = CriarOrdemServicoUseCase(os_repository=fake_repo)

    input_dto = CriarOSInputDTO(
        cpf_cnpj_cliente="12345",  # CPF inválido
        placa_veiculo="ABC-1234",
        marca_veiculo="Toyota",
        modelo_veiculo="Corolla",
        ano_veiculo=2022
    )

    with pytest.raises(ValueError, match=r"Documento \(CPF/CNPJ\) inválido"):
        use_case.executar(input_dto)
        