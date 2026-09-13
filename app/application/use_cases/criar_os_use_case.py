import uuid
from app.domain.aggregates.ordem_servico import OrdemServico
from app.domain.value_objects.cpf_cnpj import CPFCNPJ
from app.domain.value_objects.placa import PlacaVeiculo
from app.domain.repositories.os_repository import OrdemServicoRepositoryInterface
from app.application.dtos.os_dto import CriarOSInputDTO, OSOutputDTO


class CriarOrdemServicoUseCase:
    """
    Caso de Uso responsável por validar cliente/veículo e gerar uma nova OS.
    """
    def __init__(self, os_repository: OrdemServicoRepositoryInterface):
        self.os_repository = os_repository

    def executar(self, input_dto: CriarOSInputDTO) -> OSOutputDTO:
        # 1. Validações de Domínio via Value Objects
        cpf_cnpj = CPFCNPJ(input_dto.cpf_cnpj_cliente)
        placa = PlacaVeiculo(input_dto.placa_veiculo)

        # 2. Em um ambiente completo, aqui buscaríamos ou criaríamos o Cliente e o Veículo.
        # Para o ciclo da OS, geramos/atribuímos os identificadores correspondentes.
        cliente_id = uuid.uuid5(uuid.NAMESPACE_DNS, cpf_cnpj.valor)
        veiculo_id = uuid.uuid5(uuid.NAMESPACE_DNS, placa.valor)

        # 3. Instancia a Raiz do Agregado (A Ordem de Serviço nasce com status RECEBIDA)
        nova_os = OrdemServico(cliente_id=cliente_id, veiculo_id=veiculo_id)

        # 4. Persiste a nova OS utilizando a interface do repositório
        self.os_repository.salvar(nova_os)

        # 5. Retorna o DTO de saída formatado
        return OSOutputDTO(
            id=nova_os.id,
            cliente_id=nova_os.cliente_id,
            veiculo_id=nova_os.veiculo_id,
            status=nova_os.status.value,
            valor_total=nova_os.valor_total,
            data_criacao=nova_os.data_criacao,
            data_finalizacao=nova_os.data_finalizacao
        )
    