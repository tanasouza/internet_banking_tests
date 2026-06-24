# Teste de Software - Entrega Sprint 5

## BDD como linguagem de cobertura semântica

**Professor:** Dr. Claudinei de Oliveira  
**Projeto:** API Flask de Internet Banking  
**Ambiente:** Ubuntu 22.04 no WSL, Python 3.10.12  
**Ferramentas:** pytest-bdd 8.1.0 e mutmut 3.6.0

## Observação técnica sobre o mutmut

A versão 3.6.0 do mutmut identifica cada mutante por um nome completo, como
`app.x_transferencia__mutmut_24`, em vez de usar somente números.

Também foi necessário substituir os decoradores `@app.route` por registros
equivalentes usando `app.add_url_rule`. Essa mudança não alterou os endpoints
nem o comportamento da API. Ela foi necessária porque o mutmut 3.6 ignora
funções decoradas e, antes desse ajuste, não criava mutantes nas rotas Flask.

## Passo 2 - Lista bruta dos mutantes do Sprint 4

### Mutante 1 - obrigatório

**Identificador:** `app.x_transferencia__mutmut_24`

**Linha original:**

```python
if origem is None or destino is None or valor is None:
```

**Linha mutada:**

```python
if origem is None or destino is None and valor is None:
```

### Mutante 2 - obrigatório

**Identificador:** `app.x_transferencia__mutmut_39`

**Linha original:**

```python
if not isinstance(valor, (int, float)) or valor <= 0:
```

**Linha mutada:**

```python
if not isinstance(valor, (int, float)) or valor <= 1:
```

### Mutante 3 - opcional

**Identificador:** `app.x_transferencia__mutmut_62`

**Linha original:**

```python
"SELECT * FROM contas WHERE id = ?"
```

**Linha mutada:**

```python
"select * from contas where id = ?"
```

### Mutante 4 - opcional

**Identificador:** `app.x_transferencia__mutmut_63`

**Linha original:**

```python
"SELECT * FROM contas WHERE id = ?"
```

**Linha mutada:**

```python
"SELECT * FROM CONTAS WHERE ID = ?"
```

## Passo 3 - Classificação dos mutantes

### Classificação do Mutante 1

**Pergunta 1:** Sim. Existe uma entrada para a qual o original e o mutante
produzem respostas diferentes.

**Pergunta 2:** Enviar uma transferência contendo `origem=1` e `valor=100.00`,
mas sem informar `destino`. O original retorna HTTP 400. O mutante não entra na
validação de campos obrigatórios e continua o processamento até retornar HTTP
404.

**Classificação final:** INSUFICIÊNCIA DA SUÍTE.

### Classificação do Mutante 2

**Pergunta 1:** Sim.

**Pergunta 2:** Transferir R$ 0,50 da conta 2 para a conta 1. O original aceita
o valor positivo e retorna HTTP 200. O mutante considera valores menores ou
iguais a R$ 1,00 inválidos e retorna HTTP 422.

**Classificação final:** INSUFICIÊNCIA DA SUÍTE.

### Classificação do Mutante 3

**Pergunta 1:** Não.

**Pergunta 2:** Não existe entrada diferenciadora, pois o SQLite não diferencia
letras maiúsculas e minúsculas nas palavras-chave desse comando SQL.

**Classificação final:** EQUIVALENTE.

### Classificação do Mutante 4

**Pergunta 1:** Não.

**Pergunta 2:** Não existe entrada diferenciadora no banco e esquema usados,
pois o SQLite continua reconhecendo a tabela `contas` e a coluna `id`.

**Classificação final:** EQUIVALENTE.

Segundo PAPADAKIS et al. (2019, p. 286), um mutante equivalente não pode ser
morto porque a alteração sintática não produz diferença observável. A
identificação de equivalência exige análise humana, pois o problema é
indecidível em sua forma geral.

## Passo 4 - Descrição em termos de negócio

### Mutante 1

**a) Regra de negócio:** Toda transferência deve informar conta de origem,
conta de destino e valor.

**b) Entrada diferenciadora:** O cliente envia a conta de origem 1 e o valor
R$ 100,00, mas não informa a conta de destino.

**c) Resposta esperada:** HTTP 400, com a mensagem JSON:

```json
{"erro": "Campos obrigatorios ausentes: origem, destino, valor"}
```

Nenhum saldo deve ser alterado.

### Mutante 2

**a) Regra de negócio:** O internet banking deve aceitar qualquer valor
estritamente positivo quando a conta possuir saldo suficiente.

**b) Entrada diferenciadora:** A conta 2 transfere R$ 0,50 para a conta 1.

**c) Resposta esperada:** HTTP 200, com a mensagem `Transferencia realizada`.
Após a operação, os saldos seriam R$ 499,50 na conta 2 e R$ 1.000,50 na conta
1.

## Passo 5 - Conteúdo de features/transferencia.feature

```gherkin
# language: pt
Funcionalidade: Validacao de transferencias bancarias
  Como cliente do internet banking
  Quero que valores validos sejam transferidos e dados incompletos sejam recusados
  Para que minhas operacoes sejam processadas com seguranca e clareza

  Contexto:
    Dado que a conta 1 possui saldo de 1000.00
    E que a conta 2 possui saldo de 500.00

  Cenario: Aceitar transferencia de pequeno valor positivo
    Quando a conta 2 transfere 0.50 para a conta 1
    Entao a transferencia deve ser aceita com status HTTP 200
    E a mensagem deve informar "Transferencia realizada"

  Cenario: Recusar transferencia sem conta de destino
    Quando envio uma transferencia da conta 1 no valor de 100.00 sem informar o destino
    Entao a transferencia deve ser recusada com status HTTP 400
    E o erro deve informar "Campos obrigatorios ausentes: origem, destino, valor"
```

## Passo 7 - Revisão crítica do código

### a) Flask test client ou requests

O código final usa Flask test client por meio da fixture `client` definida no
`conftest.py`. Não utiliza `requests` e não depende de servidor Flask externo.
Isso mantém a arquitetura estabelecida no Sprint 4.

### b) Fixture de reset do banco

O arquivo `transferencia_steps.py` não redefine a fixture `autouse` de reset.
Uma segunda fixture de reset poderia criar duas fontes de controle sobre o
mesmo banco SQLite, causando estados divergentes ou bloqueios.

### c) Fixture client

Os steps recebem `client` como argumento e armazenam a resposta HTTP em uma
fixture de escopo de função chamada `estado_cenario`. O ajuste mantém o estado
isolado entre cenários e reutiliza a infraestrutura central do `conftest.py`.

COUTINHO e NASCIMENTO (2025) discutem benefícios e desafios da automação. Neste
projeto, o benefício só foi alcançado após revisar a saída gerada e adaptá-la
ao banco, às fixtures e ao Flask test client existentes, em vez de aceitar um
padrão genérico.

## Passo 6 - Conteúdo de features/steps/transferencia_steps.py

```python
import pytest
from pytest_bdd import given, parsers, scenarios, then, when


scenarios("../transferencia.feature")


@pytest.fixture
def estado_cenario():
    return {}


@given(parsers.parse("que a conta {conta_id:d} possui saldo de {saldo:f}"))
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
        json={"origem": origem, "destino": destino, "valor": valor},
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
```

## Passo 8 - Resultado do pytest-bdd

Comando executado:

```bash
pytest features/ -v
```

Resultado:

```text
test_aceitar_transferencia_de_pequeno_valor_positivo PASSED
test_recusar_transferencia_sem_conta_de_destino PASSED
2 passed
```

## Passo 9 - Mutation testing após o BDD

### Resultado antes dos cenários BDD

- 219 mutantes gerados;
- 165 mortos;
- 52 sobreviventes;
- 2 sem testes.

### Resultado depois dos cenários BDD

- 219 mutantes gerados;
- 182 mortos;
- 35 sobreviventes;
- 2 sem testes.

Os dois cenários BDD mataram 17 mutantes adicionais.

**Mutante 1:** `app.x_transferencia__mutmut_24` - KILLED.

**Mutante 2:** `app.x_transferencia__mutmut_39` - KILLED.

**Mutante opcional 3:** `app.x_transferencia__mutmut_62` - SURVIVED.

**Mutante opcional 4:** `app.x_transferencia__mutmut_63` - SURVIVED.

O resultado valida a classificação dos Mutantes 1 e 2 como insuficiência da
suíte. Os cenários verificaram especificamente as entradas que diferenciavam o
original dos mutantes. Os Mutantes 3 e 4 permaneceram vivos porque a mudança
de capitalização não alterou o comportamento do SQLite.

## Reflexão final

### 1. Quantos equivalentes e quantos por insuficiência?

Classifiquei dois mutantes como equivalentes e dois como insuficiência da
suíte. Essa distinção evita relatar como falha de teste uma alteração que não
produz comportamento observável. Para um gerente, isso torna a informação
sobre a capacidade detectora da suíte mais honesta.

### 2. Feature BDD comparada ao teste Python

O `transferencia.feature` pode ser entendido por gerente, auditor e analista
de negócio. O `test_ia_gerado.py` é mais adequado a desenvolvedores e
testadores. No internet banking, o BDD permite auditar as regras sem precisar
interpretar detalhes de Python.

### 3. Classificação humana e validação empírica

Os dois mutantes classificados como insuficiência foram mortos e os dois
equivalentes permaneceram vivos. Isso mostra que a classificação humana cria
uma hipótese sobre o comportamento, mas a execução empírica é necessária para
confirmá-la.

### 4. Métrica priorizada

Eu priorizaria o mutation score, pois ele verifica se a suíte percebe uma regra
errada, enquanto a cobertura de linhas apenas confirma que a linha foi
executada. Entretanto, usaria as três métricas de forma complementar, conforme
a ideia do BSTQB (2023) de empregar critérios de cobertura com diferentes
níveis de força.

### 5. BDD substitui ou complementa?

BDD complementa os testes anteriores. RAHMAN et al. (2024, p. 55-57) associam
testes precoces à detecção antecipada, ao melhor design e à manutenibilidade.
Neste projeto, os 12 testes anteriores continuaram protegendo a regressão
técnica, enquanto os dois cenários BDD acrescentaram linguagem de negócio e
mataram 17 mutantes adicionais.

### 6. Nova regulação do Banco Central

Eu revisaria primeiro o arquivo `transferencia.feature`, pois ele expressa a
regra de negócio em linguagem auditável. Depois ajustaria os steps e a
implementação para manter cenário, teste e código alinhados.

## Referências

BSTQB - BRAZILIAN SOFTWARE TESTING QUALIFICATIONS BOARD. Certified Tester
Foundation Level Syllabus: versão 4.0. 2023.

COUTINHO, N. de M.; NASCIMENTO, E. L. B. do. Desafios e benefícios da
implementação de testes automatizados em empresas de software. Cuadernos de
Educación y Desarrollo, v. 17, n. 4, e8221, 2025. DOI:
10.55905/cuadv17n4-176.

PAPADAKIS, M. et al. Mutation testing advances: an analysis and survey.
Advances in Computers, v. 112, p. 275-378, 2019. DOI:
10.1016/bs.adcom.2018.03.015.

RAHMAN, Md. S. et al. Evaluating the impact of Test-Driven Development on
Software Quality Enhancement. International Journal of Mathematical Sciences
and Computing, v. 10, n. 3, p. 51-76, 2024. DOI:
10.5815/ijmsc.2024.03.05.
