import pytest
import requests


BASE_URL = "http://127.0.0.1:5000"
TIMEOUT = 5


def test_transferencia_saldo_igual_valor():
    resposta_saldo = requests.get(f"{BASE_URL}/saldo/2", timeout=TIMEOUT)
    assert resposta_saldo.status_code == 200
    saldo_disponivel = resposta_saldo.json()["saldo"]

    try:
        resposta = requests.post(
            f"{BASE_URL}/transferencia",
            json={"origem": 2, "destino": 1, "valor": saldo_disponivel},
            timeout=TIMEOUT,
        )

        assert resposta.status_code == 200
        assert resposta.json()["mensagem"] == "Transferencia realizada"
        assert resposta.json()["valor"] == pytest.approx(saldo_disponivel)
    finally:
        requests.post(
            f"{BASE_URL}/transferencia",
            json={"origem": 1, "destino": 2, "valor": saldo_disponivel},
            timeout=TIMEOUT,
        )


def test_transferencia_sucesso():
    try:
        resposta = requests.post(
            f"{BASE_URL}/transferencia",
            json={"origem": 2, "destino": 1, "valor": 100.00},
            timeout=TIMEOUT,
        )

        assert resposta.status_code == 200
        assert resposta.json()["mensagem"] == "Transferencia realizada"
        assert resposta.json()["valor"] == pytest.approx(100.00)
    finally:
        requests.post(
            f"{BASE_URL}/transferencia",
            json={"origem": 1, "destino": 2, "valor": 100.00},
            timeout=TIMEOUT,
        )


def test_transferencia_saldo_insuficiente():
    resposta = requests.post(
        f"{BASE_URL}/transferencia",
        json={"origem": 3, "destino": 1, "valor": 500.00},
        timeout=TIMEOUT,
    )

    assert resposta.status_code == 422
    assert resposta.json()["erro"] == "Saldo insuficiente"
    assert resposta.json()["saldo_atual"] == pytest.approx(0.00)


def test_transferencia_conta_origem_inexistente():
    resposta = requests.post(
        f"{BASE_URL}/transferencia",
        json={"origem": 999, "destino": 1, "valor": 100.00},
        timeout=TIMEOUT,
    )

    assert resposta.status_code == 404
    assert resposta.json()["erro"] == "Conta nao encontrada"


def test_transferencia_conta_destino_inexistente():
    resposta = requests.post(
        f"{BASE_URL}/transferencia",
        json={"origem": 1, "destino": 999, "valor": 100.00},
        timeout=TIMEOUT,
    )

    assert resposta.status_code == 404
    assert resposta.json()["erro"] == "Conta nao encontrada"


def test_transferencia_valor_negativo():
    resposta = requests.post(
        f"{BASE_URL}/transferencia",
        json={"origem": 1, "destino": 2, "valor": -100},
        timeout=TIMEOUT,
    )

    assert resposta.status_code == 422
    assert resposta.json()["erro"] == "Valor deve ser positivo"


def test_transferencia_valor_zero():
    resposta = requests.post(
        f"{BASE_URL}/transferencia",
        json={"origem": 1, "destino": 2, "valor": 0},
        timeout=TIMEOUT,
    )

    assert resposta.status_code == 422
    assert resposta.json()["erro"] == "Valor deve ser positivo"


def test_transferencia_mesma_conta():
    resposta = requests.post(
        f"{BASE_URL}/transferencia",
        json={"origem": 1, "destino": 1, "valor": 100.00},
        timeout=TIMEOUT,
    )

    assert resposta.status_code == 422
    assert resposta.json()["erro"] == "Origem e destino nao podem ser iguais"


def test_saldo_conta_existente():
    resposta = requests.get(f"{BASE_URL}/saldo/1", timeout=TIMEOUT)
    dados = resposta.json()

    assert resposta.status_code == 200
    assert dados["conta_id"] == 1
    assert dados["titular"] == "Alice"
    assert isinstance(dados["saldo"], (int, float))


def test_saldo_conta_inexistente():
    resposta = requests.get(f"{BASE_URL}/saldo/999", timeout=TIMEOUT)

    assert resposta.status_code == 404
    assert resposta.json()["erro"] == "Conta nao encontrada"


def test_extrato_conta_existente():
    resposta = requests.get(f"{BASE_URL}/extrato/1", timeout=TIMEOUT)
    dados = resposta.json()

    assert resposta.status_code == 200
    assert dados["conta_id"] == 1
    assert dados["titular"] == "Alice"
    assert isinstance(dados["saldo_atual"], (int, float))
    assert isinstance(dados["historico"], list)


def test_extrato_conta_inexistente():
    resposta = requests.get(f"{BASE_URL}/extrato/999", timeout=TIMEOUT)

    assert resposta.status_code == 404
    assert resposta.json()["erro"] == "Conta nao encontrada"
