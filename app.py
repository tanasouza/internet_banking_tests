# Claudinei de Oliveira - Pt-br - UTF-8
# app2.py — Sistema de Internet Banking (versão Sprint 4)
#
# Esta versão é IDÊNTICA ao app.py dos Sprints 1, 2 e 3 em todas as rotas
# e regras de negócio. A única diferença é que o caminho do banco SQLite
# agora vem de uma configuração externa, carregada via app.config a partir
# do arquivo config.py. Essa externalização é o que permite ao Flask test
# client importar o app diretamente, sem servidor HTTP, e ao mutmut medir
# os testes — pré-requisito técnico do Sprint 4.
#
# Procedimento (conforme roteiro Sprint 4):
#   1. Baixe este arquivo e o config.py.
#   2. Cole ambos na pasta internet_banking_tests.
#   3. Renomeie app2.py para app.py (substituindo o app.py atual).
#   4. NÃO renomeie o config.py — o app procura por esse nome exato.

# Endpoints disponíveis em http://127.0.0.1:5000
#   GET  /saldo/<conta_id>
#   POST /transferencia    corpo: {"origem": int, "destino": int, "valor": float}
#   GET  /extrato/<conta_id>

from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)
SQLITE_INT_MIN = -(2**63)
SQLITE_INT_MAX = 2**63 - 1

# ----------------------------------------------------------------------
# Carregamento da configuração externa.
#
# A classe Config está em config.py (mesma pasta). Após esta linha,
# app.config['DATABASE'] está populado com o valor definido lá.
#
# Sprint 4: o conftest.py pode sobrescrever app.config para apontar
# para a TestConfig (ex.: app.config.from_object('config.TestConfig')),
# isolando o ambiente de mutation testing sem editar este arquivo.
# ----------------------------------------------------------------------
app.config.from_object('config.Config')


@app.errorhandler(404)
def pagina_nao_encontrada(_erro):
    return jsonify({"erro": "Conta nao encontrada"}), 404


# BANCO DE DADOS
def get_db():
    # Abre e retorna uma conexão com o banco SQLite cujo caminho está
    # em app.config['DATABASE']. O valor vem de config.py.
    conn = sqlite3.connect(app.config["DATABASE"])
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    # Cria as tabelas e insere os dados iniciais se ainda não existirem.
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS contas (
            id      INTEGER PRIMARY KEY,
            titular TEXT    NOT NULL,
            saldo   REAL    NOT NULL CHECK(saldo >= 0)
        );

        CREATE TABLE IF NOT EXISTS transferencias (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            origem    INTEGER NOT NULL,
            destino   INTEGER NOT NULL,
            valor     REAL    NOT NULL,
            data_hora TEXT    NOT NULL,
            FOREIGN KEY (origem)  REFERENCES contas(id),
            FOREIGN KEY (destino) REFERENCES contas(id)
        );

        INSERT OR IGNORE INTO contas (id, titular, saldo) VALUES (1, 'Alice',  1000.00);
        INSERT OR IGNORE INTO contas (id, titular, saldo) VALUES (2, 'Bob',     500.00);
        INSERT OR IGNORE INTO contas (id, titular, saldo) VALUES (3, 'Carlos',    0.00);
    """)
    conn.commit()
    conn.close()


def conta_id_suportado(conta_id):
    return SQLITE_INT_MIN <= conta_id <= SQLITE_INT_MAX


# ENDPOINT: GET /saldo/<conta_id>
def saldo(conta_id):
    """
    Retorna o saldo atual de uma conta.
    Respostas:
        200  {"conta_id": int, "titular": str, "saldo": float}
        404  {"erro": "Conta nao encontrada"}
    """
    if not conta_id_suportado(conta_id):
        return jsonify({"erro": "Conta nao encontrada"}), 404

    conn = get_db()
    conta = conn.execute(
        "SELECT * FROM contas WHERE id = ?", (conta_id,)
    ).fetchone()
    conn.close()

    if conta is None:
        return jsonify({"erro": "Conta nao encontrada"}), 404

    return jsonify({
        "conta_id": conta_id,
        "titular":  conta["titular"],
        "saldo":    conta["saldo"]
    }), 200


# ENDPOINT: POST /transferencia
def transferencia():
    """
    Realiza uma transferência entre duas contas.

    Corpo esperado (JSON):
        {"origem": int, "destino": int, "valor": float}
    Respostas:
        200  {"mensagem": "Transferencia realizada", "valor": float}
        400  {"erro": "Corpo da requisicao invalido ou ausente"}
        400  {"erro": "Campos obrigatorios ausentes: origem, destino, valor"}
        404  {"erro": "Conta nao encontrada"}
        422  {"erro": "Valor deve ser positivo"}
        422  {"erro": "Origem e destino nao podem ser iguais"}
        422  {"erro": "Saldo insuficiente", "saldo_atual": float}
        500  {"erro": "Erro interno", "detalhe": str}
    """
    dados = request.get_json(silent=True)

    # Valida presença e formato do corpo
    if dados is None or not isinstance(dados, dict):
        return jsonify({"erro": "Corpo da requisicao invalido ou ausente"}), 400

    origem  = dados.get("origem")
    destino = dados.get("destino")
    valor   = dados.get("valor")

    # Valida campos obrigatórios
    if origem is None or destino is None or valor is None:
        return jsonify({"erro": "Campos obrigatorios ausentes: origem, destino, valor"}), 400

    # Valida valor positivo
    if not isinstance(valor, (int, float)) or valor <= 0:
        return jsonify({"erro": "Valor deve ser positivo"}), 422

    # Valida contas distintas
    if origem == destino:
        return jsonify({"erro": "Origem e destino nao podem ser iguais"}), 422

    # Valida faixa suportada pelo SQLite para chaves inteiras.
    if (
        not isinstance(origem, int)
        or not isinstance(destino, int)
        or not conta_id_suportado(origem)
        or not conta_id_suportado(destino)
    ):
        return jsonify({"erro": "Conta nao encontrada"}), 404

    conn = get_db()
    try:
        conta_origem  = conn.execute(
            "SELECT * FROM contas WHERE id = ?", (origem,)
        ).fetchone()
        conta_destino = conn.execute(
            "SELECT * FROM contas WHERE id = ?", (destino,)
        ).fetchone()

        # Valida existência das contas
        if conta_origem is None or conta_destino is None:
            return jsonify({"erro": "Conta nao encontrada"}), 404

        # Valida saldo suficiente
        if conta_origem["saldo"] < valor:
            return jsonify({
                "erro":        "Saldo insuficiente",
                "saldo_atual": conta_origem["saldo"]
            }), 422

        # Executa a transferência
        conn.execute(
            "UPDATE contas SET saldo = saldo - ? WHERE id = ?", (valor, origem)
        )
        conn.execute(
            "UPDATE contas SET saldo = saldo + ? WHERE id = ?", (valor, destino)
        )
        conn.execute(
            "INSERT INTO transferencias (origem, destino, valor, data_hora) "
            "VALUES (?, ?, ?, ?)",
            (origem, destino, valor, datetime.now().isoformat())
        )
        conn.commit()

        return jsonify({
            "mensagem": "Transferencia realizada",
            "valor":    valor
        }), 200

    except Exception as e:
        conn.rollback()
        return jsonify({"erro": "Erro interno", "detalhe": str(e)}), 500

    finally:
        conn.close()


# ENDPOINT: GET /extrato/<conta_id>
def extrato(conta_id):
    """
    Retorna o histórico de transferências de uma conta.

    Respostas:
        200  {"conta_id": int, "titular": str, "saldo_atual": float,
               "historico": [{"id", "origem", "destino", "valor", "data_hora"}]}
        404  {"erro": "Conta nao encontrada"}
    """
    if not conta_id_suportado(conta_id):
        return jsonify({"erro": "Conta nao encontrada"}), 404

    conn = get_db()

    conta = conn.execute(
        "SELECT * FROM contas WHERE id = ?", (conta_id,)
    ).fetchone()

    if conta is None:
        conn.close()
        return jsonify({"erro": "Conta nao encontrada"}), 404

    historico = conn.execute(
        "SELECT * FROM transferencias "
        "WHERE origem = ? OR destino = ? "
        "ORDER BY data_hora DESC",
        (conta_id, conta_id)
    ).fetchall()
    conn.close()

    return jsonify({
        "conta_id":   conta_id,
        "titular":    conta["titular"],
        "saldo_atual": conta["saldo"],
        "historico":  [dict(r) for r in historico]
    }), 200


app.add_url_rule(
    "/saldo/<int:conta_id>",
    endpoint="saldo",
    view_func=saldo,
    methods=["GET"],
)
app.add_url_rule(
    "/transferencia",
    endpoint="transferencia",
    view_func=transferencia,
    methods=["POST"],
)
app.add_url_rule(
    "/extrato/<int:conta_id>",
    endpoint="extrato",
    view_func=extrato,
    methods=["GET"],
)


if __name__ == "__main__":
    init_db()
    print("\nSistema de Internet Banking iniciado.")
    print("Contas disponíveis: 1 (Alice / R$ 1000,00), 2 (Bob / R$ 500,00), 3 (Carlos / R$ 0,00)")
    print(f"Banco de dados (de config.py): {app.config['DATABASE']}")
    print("Acesse: http://127.0.0.1:5000\n")
    app.run(debug=True, port=5000)
