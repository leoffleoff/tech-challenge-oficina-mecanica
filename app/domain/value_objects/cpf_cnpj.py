import re

class CPFCNPJ:
    """
    Value Object imutável que garante a consistência do documento do cliente.
    """
    def __init__(self, valor: str):
        cleaned_valor = re.sub(r'\D', '', valor or '')
        if not self._validar(cleaned_valor):
            raise ValueError(f"Documento (CPF/CNPJ) inválido: {valor}")
        
        self._valor = cleaned_valor

    @property
    def valor(self) -> str:
        return self._valor

    def _validar(self, documento: str) -> bool:
        # Validação simples de tamanho (8 a 14 dígitos para fins de MVP)
        # Permite extensões futuras para o cálculo oficial de dígitos verificadores
        return len(documento) in (11, 14) and not documento == documento[0] * len(documento)

    def __eq__(self, other) -> bool:
        return isinstance(other, CPFCNPJ) and self._valor == other._valor

    def __str__(self) -> str:
        return self._valor
    