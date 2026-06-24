# Resultados do mutmut antes dos cenarios BDD

Ambiente: Ubuntu 22.04 no WSL, Python 3.10.12, mutmut 3.6.0.

Comando:

```bash
source .venv-linux/bin/activate
mutmut run
mutmut results
```

Resumo da execucao:

- 219 mutantes gerados.
- 165 mutantes mortos.
- 52 mutantes sobreviventes.
- 2 mutantes sem testes, ambos em `init_db()`.

Mutantes selecionados para o Sprint 5:

1. `app.x_transferencia__mutmut_24` - `survived`
   - Original: `if origem is None or destino is None or valor is None:`
   - Mutado: `if origem is None or destino is None and valor is None:`
2. `app.x_transferencia__mutmut_39` - `survived`
   - Original: `if not isinstance(valor, (int, float)) or valor <= 0:`
   - Mutado: `if not isinstance(valor, (int, float)) or valor <= 1:`
3. `app.x_transferencia__mutmut_62` - `survived`
   - Original: `"SELECT * FROM contas WHERE id = ?"`
   - Mutado: `"select * from contas where id = ?"`
4. `app.x_transferencia__mutmut_63` - `survived`
   - Original: `"SELECT * FROM contas WHERE id = ?"`
   - Mutado: `"SELECT * FROM CONTAS WHERE ID = ?"`
