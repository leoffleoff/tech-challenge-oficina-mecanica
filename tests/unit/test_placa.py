import pytest
from app.domain.value_objects.placa import PlacaVeiculo


def test_placa_padrao_antigo_valida():
    placa = PlacaVeiculo("ABC-1234")
    assert placa.valor == "ABC1234"


def test_placa_padrao_mercosul_valida():
    placa = PlacaVeiculo("abc1d23")
    assert placa.valor == "ABC1D23"


def test_erro_placa_formato_invalido():
    with pytest.raises(ValueError, match="Placa de veículo inválida"):
        PlacaVeiculo("AB12345")


def test_erro_placa_com_caracteres_especiais_invalidos():
    with pytest.raises(ValueError, match="Placa de veículo inválida"):
        PlacaVeiculo("ABC@123")


def test_igualdade_entre_placas():
    placa1 = PlacaVeiculo("abc-1234")
    placa2 = PlacaVeiculo("ABC1234")
    assert placa1 == placa2
    