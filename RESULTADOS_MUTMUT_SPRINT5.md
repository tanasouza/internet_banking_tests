# Resultados do mutmut depois dos cenarios BDD

Ambiente: Ubuntu 22.04 no WSL, Python 3.10.12, mutmut 3.6.0.

Suite executada:

```bash
pytest test_flask_client.py features/ -q
```

Resultado funcional:

```text
14 passed
```

Resumo da nova medicao:

- 219 mutantes gerados.
- 182 mutantes mortos.
- 35 mutantes sobreviventes.
- 2 mutantes sem testes.
- Os cenarios BDD mataram 17 mutantes adicionais.

Status dos mutantes selecionados:

1. `app.x_transferencia__mutmut_24`: `killed`
2. `app.x_transferencia__mutmut_39`: `killed`
3. `app.x_transferencia__mutmut_62`: `survived`
4. `app.x_transferencia__mutmut_63`: `survived`

Conclusao:

Os mutantes 24 e 39 eram insuficiencias reais da suite. Entradas concretas
produziam respostas diferentes entre o original e o mutado, e os cenarios
Gherkin correspondentes os mataram. Os mutantes 62 e 63 permaneceram vivos
porque o SQLite trata palavras-chave e identificadores SQL sem distinguir
maiusculas de minusculas nesses comandos.
