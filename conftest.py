from pathlib import Path
import sqlite3

import pytest

from app import app


DATABASE = Path(__file__).resolve().parent / "banking.db"
app.config["DATABASE"] = str(DATABASE)
app.config["TESTING"] = True


def criar_estrutura(conexao):
    conexao.executescript(
        """
        CREATE TABLE IF NOT EXISTS contas (
            id INTEGER PRIMARY KEY,
            titular TEXT NOT NULL,
            saldo REAL NOT NULL CHECK(saldo >= 0)
        );

        CREATE TABLE IF NOT EXISTS transferencias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            origem INTEGER NOT NULL,
            destino INTEGER NOT NULL,
            valor REAL NOT NULL,
            data_hora TEXT NOT NULL,
            FOREIGN KEY (origem) REFERENCES contas(id),
            FOREIGN KEY (destino) REFERENCES contas(id)
        );
        """
    )


@pytest.fixture(autouse=True)
def resetar_banco():
    conexao = sqlite3.connect(DATABASE)

    try:
        criar_estrutura(conexao)
        conexao.execute("DELETE FROM transferencias")
        conexao.execute("DELETE FROM contas")
        conexao.executemany(
            "INSERT INTO contas (id, titular, saldo) VALUES (?, ?, ?)",
            [
                (1, "Alice", 1000.00),
                (2, "Bob", 500.00),
                (3, "Carlos", 0.00),
            ],
        )
        conexao.execute(
            "DELETE FROM sqlite_sequence WHERE name = 'transferencias'"
        )
        conexao.commit()
    finally:
        conexao.close()

    yield


@pytest.fixture
def client():
    with app.test_client() as cliente:
        yield cliente
