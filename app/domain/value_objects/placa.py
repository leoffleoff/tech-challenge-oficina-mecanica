import re

class PlacaVeiculo:
    """
    Value Object imutável que valida o formato da placa (padrão antigo e Mercosul).
    """
    # Aceita ABC1234 (Antigo) ou ABC1D23 (Mercosul)
    PADRAO_PLACA = re.compile(r'^[A-Z]{3}[0-9][A-Z0-9][0-9]{2}$')

    def __init__(self, placa: str):
        placa_limpa = (placa or '').strip().upper().replace("-", "")
        if not self.PADRAO_PLACA.match(placa_limpa):
            raise ValueError(f"Placa de veículo inválida: {placa}")
        
        self._valor = placa_limpa

    @property
    def valor(self) -> str:
        return self._valor

    def __eq__(self, other) -> bool:
        return isinstance(other, PlacaVeiculo) and self._valor == other._valor

    def __str__(self) -> str:
        return self._valor
    