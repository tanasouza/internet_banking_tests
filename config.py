# Claudinei de Oliveira - Pt-br - UTF-8
# config.py — Configuração externa do Sistema de Internet Banking (Sprint 4)
#
# Este é o arquivo que DEFINE o valor de app.config['DATABASE'] lido pelo
# app2.py via app.config.from_object('config.Config').
#
# Por que separar a configuração do app:
#   - Permite ao Flask test client (Sprint 4) substituir o caminho do banco
#     em tempo de teste sem editar o app.py.
#   - Permite ao mutmut executar os testes contra mutantes do app.py sem
#     que cada mutante carregue um caminho de banco diferente.
#   - É o padrão profissional Flask de externalização de configuração
#     (Application Configuration via Object).
#
# Procedimento (conforme roteiro Sprint 4):
#   1. Cole este arquivo na pasta internet_banking_tests, ao lado do app.py.
#   2. NÃO renomeie — o app2.py procura por 'config.py' com este nome exato.
#   3. NÃO comite o banking.db gerado em tempo de execução (use .gitignore).
#
# Uso pelo app2.py (já configurado lá):
#   app.config.from_object('config.Config')
#
# Uso opcional pelo conftest.py (para isolar o ambiente de testes):
#   app.config.from_object('config.TestConfig')


from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


class Config:
    """
    Configuração padrão (runtime).
    Esta é a classe carregada pelo app2.py em condições normais de execução.
    """

    # Caminho do banco SQLite — lido por app.config['DATABASE'] no app2.py.
    # Mantenha "banking.db" para preservar continuidade com os Sprints 1, 2 e 3.
    DATABASE = str(BASE_DIR / "banking.db")

    # Modo de teste do Flask — False em runtime.
    TESTING = False


class TestConfig(Config):
    """
    Configuração específica para mutation testing (Sprint 4).

    Herda de Config e sobrescreve apenas o que precisa ser diferente
    durante a execução do pytest/mutmut. Por padrão, mantém o mesmo
    banking.db dos sprints anteriores; o isolamento entre execuções é
    garantido pela fixture autouse de reset no conftest.py do Sprint 2.

    Para isolar fisicamente o banco de testes (opcional, recomendado para
    runs longos do mutmut), descomente a linha abaixo:
    """

    TESTING = True
    # DATABASE = "banking_test.db"   # descomente para banco de teste isolado
