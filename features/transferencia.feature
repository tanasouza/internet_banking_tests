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
