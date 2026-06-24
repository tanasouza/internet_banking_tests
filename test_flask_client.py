import pytest

from app import app


app.config["TESTING"] = True


def test_transferencia_saldo_igual_valor():
    cliente = app.test_client()
    resposta_saldo = cliente.get("/saldo/2")

    assert resposta_saldo.status_code == 200
    saldo_disponivel = resposta_saldo.get_json()["saldo"]

    resposta = cliente.post(
        "/transferencia",
        json={"origem": 2, "destino": 1, "valor": saldo_disponivel},
    )

    assert resposta.status_code == 200
    assert resposta.get_json()["mensagem"] == "Transferencia realizada"
    assert resposta.get_json()["valor"] == pytest.approx(saldo_disponivel)


def test_transferencia_sucesso():
    cliente = app.test_client()
    resposta = cliente.post(
        "/transferencia",
        json={"origem": 2, "destino": 1, "valor": 100.00},
    )

    assert resposta.status_code == 200
    assert resposta.get_json()["mensagem"] == "Transferencia realizada"
    assert resposta.get_json()["valor"] == pytest.approx(100.00)


def test_transferencia_saldo_insuficiente():
    cliente = app.test_client()
    resposta = cliente.post(
        "/transferencia",
        json={"origem": 3, "destino": 1, "valor": 500.00},
    )

    assert resposta.status_code == 422
    assert resposta.get_json()["erro"] == "Saldo insuficiente"
    assert resposta.get_json()["saldo_atual"] == pytest.approx(0.00)


def test_transferencia_conta_origem_inexistente():
    cliente = app.test_client()
    resposta = cliente.post(
        "/transferencia",
        json={"origem": 999, "destino": 1, "valor": 100.00},
    )

    assert resposta.status_code == 404
    assert resposta.get_json()["erro"] == "Conta nao encontrada"


def test_transferencia_conta_destino_inexistente():
    cliente = app.test_client()
    resposta = cliente.post(
        "/transferencia",
        json={"origem": 1, "destino": 999, "valor": 100.00},
    )

    assert resposta.status_code == 404
    assert resposta.get_json()["erro"] == "Conta nao encontrada"


def test_transferencia_valor_negativo():
    cliente = app.test_client()
    resposta = cliente.post(
        "/transferencia",
        json={"origem": 1, "destino": 2, "valor": -100},
    )

    assert resposta.status_code == 422
    assert resposta.get_json()["erro"] == "Valor deve ser positivo"


def test_transferencia_valor_zero():
    cliente = app.test_client()
    resposta = cliente.post(
        "/transferencia",
        json={"origem": 1, "destino": 2, "valor": 0},
    )

    assert resposta.status_code == 422
    assert resposta.get_json()["erro"] == "Valor deve ser positivo"


def test_transferencia_mesma_conta():
    cliente = app.test_client()
    resposta = cliente.post(
        "/transferencia",
        json={"origem": 1, "destino": 1, "valor": 100.00},
    )

    assert resposta.status_code == 422
    assert resposta.get_json()["erro"] == (
        "Origem e destino nao podem ser iguais"
    )


def test_saldo_conta_existente():
    cliente = app.test_client()
    resposta = cliente.get("/saldo/1")
    dados = resposta.get_json()

    assert resposta.status_code == 200
    assert dados["conta_id"] == 1
    assert dados["titular"] == "Alice"
    assert dados["saldo"] == pytest.approx(1000.00)


def test_saldo_conta_inexistente():
    cliente = app.test_client()
    resposta = cliente.get("/saldo/999")

    assert resposta.status_code == 404
    assert resposta.get_json()["erro"] == "Conta nao encontrada"


def test_extrato_conta_existente():
    cliente = app.test_client()
    resposta = cliente.get("/extrato/1")
    dados = resposta.get_json()

    assert resposta.status_code == 200
    assert dados["conta_id"] == 1
    assert dados["titular"] == "Alice"
    assert dados["saldo_atual"] == pytest.approx(1000.00)
    assert dados["historico"] == []


def test_extrato_conta_inexistente():
    cliente = app.test_client()
    resposta = cliente.get("/extrato/999")

    assert resposta.status_code == 404
    assert resposta.get_json()["erro"] == "Conta nao encontrada"
