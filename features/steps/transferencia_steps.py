import pytest
from pytest_bdd import given, parsers, scenarios, then, when


scenarios("../transferencia.feature")


@pytest.fixture
def estado_cenario():
    return {}


@given(
    parsers.parse(
        "que a conta {conta_id:d} possui saldo de {saldo:f}"
    )
)
def verificar_saldo_inicial(client, conta_id, saldo):
    resposta = client.get(f"/saldo/{conta_id}")

    assert resposta.status_code == 200
    assert resposta.get_json()["saldo"] == pytest.approx(saldo)


@when(
    parsers.parse(
        "a conta {origem:d} transfere {valor:f} para a conta {destino:d}"
    )
)
def transferir_valor(client, estado_cenario, origem, destino, valor):
    estado_cenario["resposta"] = client.post(
        "/transferencia",
        json={
            "origem": origem,
            "destino": destino,
            "valor": valor,
        },
    )


@when(
    parsers.parse(
        "envio uma transferencia da conta {origem:d} no valor de {valor:f} "
        "sem informar o destino"
    )
)
def transferir_sem_destino(client, estado_cenario, origem, valor):
    estado_cenario["resposta"] = client.post(
        "/transferencia",
        json={"origem": origem, "valor": valor},
    )


@then(
    parsers.parse(
        "a transferencia deve ser aceita com status HTTP {status:d}"
    )
)
def verificar_transferencia_aceita(estado_cenario, status):
    assert estado_cenario["resposta"].status_code == status


@then(
    parsers.parse(
        "a transferencia deve ser recusada com status HTTP {status:d}"
    )
)
def verificar_transferencia_recusada(estado_cenario, status):
    assert estado_cenario["resposta"].status_code == status


@then(parsers.parse('a mensagem deve informar "{mensagem}"'))
def verificar_mensagem(estado_cenario, mensagem):
    assert estado_cenario["resposta"].get_json()["mensagem"] == mensagem


@then(parsers.parse('o erro deve informar "{erro}"'))
def verificar_erro(estado_cenario, erro):
    assert estado_cenario["resposta"].get_json()["erro"] == erro
