import pytest
import requests
from hypothesis import given, strategies as st, settings, assume


BASE_URL = "http://127.0.0.1:5000"
TIMEOUT = 5


@settings(max_examples=30)
@given(
    valor=st.one_of(
        st.just(-0.001),
        st.floats(
            min_value=-1_000_000.0,
            max_value=0.0,
            allow_nan=False,
            allow_infinity=False,
        ),
    )
)
def test_transferencia_valor_nao_positivo_retorna_422(valor):
    resposta = requests.post(
        f"{BASE_URL}/transferencia",
        json={"origem": 1, "destino": 2, "valor": valor},
        timeout=TIMEOUT,
    )

    assert resposta.status_code == 422


@settings(max_examples=30)
@given(
    conta_id=st.one_of(
        st.just(9223372036854775808),
        st.integers(),
    )
)
def test_saldo_conta_inexistente_retorna_404(conta_id):
    assume(conta_id not in {1, 2, 3})

    resposta = requests.get(
        f"{BASE_URL}/saldo/{conta_id}",
        timeout=TIMEOUT,
    )

    assert resposta.status_code == 404


@settings(max_examples=30)
@given(
    origem=st.integers(min_value=1, max_value=2),
    destino=st.integers(min_value=1, max_value=3),
    valor=st.floats(
        min_value=0.001,
        max_value=500.0,
        allow_nan=False,
        allow_infinity=False,
    ),
)
def test_transferencia_preserva_soma_dos_saldos(origem, destino, valor):
    assume(origem != destino)

    resposta_origem_antes = requests.get(
        f"{BASE_URL}/saldo/{origem}",
        timeout=TIMEOUT,
    )
    resposta_destino_antes = requests.get(
        f"{BASE_URL}/saldo/{destino}",
        timeout=TIMEOUT,
    )

    assert resposta_origem_antes.status_code == 200
    assert resposta_destino_antes.status_code == 200

    saldo_origem_antes = resposta_origem_antes.json()["saldo"]
    saldo_destino_antes = resposta_destino_antes.json()["saldo"]
    assume(valor <= saldo_origem_antes)

    resposta_transferencia = requests.post(
        f"{BASE_URL}/transferencia",
        json={"origem": origem, "destino": destino, "valor": valor},
        timeout=TIMEOUT,
    )
    assume(resposta_transferencia.status_code == 200)

    try:
        resposta_origem_depois = requests.get(
            f"{BASE_URL}/saldo/{origem}",
            timeout=TIMEOUT,
        )
        resposta_destino_depois = requests.get(
            f"{BASE_URL}/saldo/{destino}",
            timeout=TIMEOUT,
        )

        assert resposta_origem_depois.status_code == 200
        assert resposta_destino_depois.status_code == 200

        saldo_origem_depois = resposta_origem_depois.json()["saldo"]
        saldo_destino_depois = resposta_destino_depois.json()["saldo"]

        soma_antes = saldo_origem_antes + saldo_destino_antes
        soma_depois = saldo_origem_depois + saldo_destino_depois

        assert soma_depois == pytest.approx(soma_antes)
    finally:
        resposta_reversao = requests.post(
            f"{BASE_URL}/transferencia",
            json={"origem": destino, "destino": origem, "valor": valor},
            timeout=TIMEOUT,
        )
        assert resposta_reversao.status_code == 200
