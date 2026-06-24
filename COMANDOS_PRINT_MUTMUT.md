# Comandos para os prints

## Abrir o Ubuntu e ativar o ambiente

No PowerShell:

```powershell
wsl -d Ubuntu-22.04
```

No Ubuntu:

```bash
cd ~/internet_banking_test
source .venv-linux/bin/activate
```

## Print do pytest-bdd - Passo 8

```bash
pytest features/ -v
```

Resultado esperado:

```text
2 passed
```

## Reproduzir o resultado do Sprint 4

Esta execução usa somente os 12 testes do `test_flask_client.py`.

```bash
cp setup_sprint4.cfg setup.cfg
rm -rf .mutmut-cache mutants
mutmut run
mutmut results
```

Resultados obtidos anteriormente:

```text
219 mutantes
165 killed
52 survived
2 no tests
```

Para mostrar os quatro mutantes selecionados:

```bash
mutmut show app.x_transferencia__mutmut_24
mutmut show app.x_transferencia__mutmut_39
mutmut show app.x_transferencia__mutmut_62
mutmut show app.x_transferencia__mutmut_63
```

Antes do BDD, os quatro aparecem como `survived`.

## Reproduzir o resultado do Sprint 5

Esta execução usa os 12 testes Flask client e os dois cenários BDD.

```bash
cp setup_sprint5.cfg setup.cfg
rm -rf .mutmut-cache mutants
mutmut run
mutmut results
```

Resultados obtidos anteriormente:

```text
219 mutantes
182 killed
35 survived
2 no tests
```

Mostrar os mutantes obrigatórios depois do BDD:

```bash
mutmut show app.x_transferencia__mutmut_24
mutmut show app.x_transferencia__mutmut_39
```

Resultado esperado:

```text
app.x_transferencia__mutmut_24: killed
app.x_transferencia__mutmut_39: killed
```

Mostrar os opcionais equivalentes:

```bash
mutmut show app.x_transferencia__mutmut_62
mutmut show app.x_transferencia__mutmut_63
```

Resultado esperado:

```text
app.x_transferencia__mutmut_62: survived
app.x_transferencia__mutmut_63: survived
```

## Melhor organização dos prints

Tire três prints separados:

1. `pytest features/ -v`, mostrando os dois cenários como `PASSED`.
2. `mutmut results`, mostrando a lista final de sobreviventes.
3. Os dois comandos `mutmut show` dos mutantes 24 e 39, mostrando `killed`.
