import pytest
from app.domain.value_objects.cpf_cnpj import CPFCNPJ


def test_cpf_valido_somente_numeros():
    doc = CPFCNPJ("12345678901")
    assert doc.valor == "12345678901"
    assert str(doc) == "12345678901"


def test_cpf_valido_com_mascara_e_formatacao():
    doc = CPFCNPJ("123.456.789-01")
    assert doc.valor == "12345678901"


def test_cnpj_valido():
    doc = CPFCNPJ("12.345.678/0001-95")
    assert doc.valor == "12345678000195"


def test_erro_documento_com_tamanho_invalido():
    with pytest.raises(ValueError, match=r"Documento \(CPF/CNPJ\) inválido"):
        CPFCNPJ("12345")


def test_erro_documento_com_digitos_repetidos():
    with pytest.raises(ValueError, match=r"Documento \(CPF/CNPJ\) inválido"):
        CPFCNPJ("11111111111")


def test_igualdade_entre_value_objects():
    doc1 = CPFCNPJ("123.456.789-01")
    doc2 = CPFCNPJ("12345678901")
    assert doc1 == doc2
    