# Matriz de rastreabilidade - Sprint 8

| ID | Requisito | Caso de teste | Artefato | Evidencia |
|---|---|---|---|---|
| TC-S1-001 | REQ-TRF-001 - Transferir valor total disponivel quando ha saldo suficiente | test_transferencia_saldo_igual_valor | test_ia_gerado.py / test_flask_client.py | PASSED em 0.028s |
| TC-S3-001 | REQ-TRF-002 - Recusar valor zero ou negativo | test_transferencia_valor_nao_positivo_retorna_422 | test_hypothesis.py | PASSED em 0.285s |
| TC-S4-001 | REQ-TRF-003 - Recusar conta inexistente | test_transferencia_conta_origem_inexistente | test_flask_client.py | PASSED em 0.013s |
| TC-S5-001 | REQ-TRF-004 - Aceitar qualquer valor positivo com saldo suficiente | test_aceitar_transferencia_de_pequeno_valor_positivo | features/transferencia.feature | PASSED em 0.026s |
| TC-S5-002 | REQ-TRF-005 - Recusar transferencia com campo obrigatorio ausente | test_recusar_transferencia_sem_conta_de_destino | features/transferencia.feature | PASSED em 0.018s |
