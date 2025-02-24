menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo_conta = 0  
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3 

while True:

    opcao = input(menu)

    if opcao == "d":
        valor = float(input("Informe o valor do depósito: "))

        if valor > 0:
            saldo_conta += valor  
            extrato += f"Depósito: R$ {valor:.2f} | Saldo após depósito: R$ {saldo_conta:.2f}\n"
            print(f"Depósito realizado com sucesso! Saldo da conta: R$ {saldo_conta:.2f}")
        else:
            print("Operação falhou! O valor informado é inválido.")

    elif opcao == "s":
        valor = float(input("Informe o valor do saque: "))

        excedeu_saldo = valor > saldo_conta
        excedeu_limite = valor > limite
        excedeu_saques = numero_saques >= LIMITE_SAQUES

        if excedeu_saldo:
            print("Operação falhou! Você não tem saldo suficiente.")
        elif excedeu_limite:
            print("Operação falhou! O valor do saque excede o limite.")
        elif excedeu_saques:
            print("Operação falhou! Número máximo de saques excedido.")
        elif valor > 0:
            saldo_conta -= valor  # O saque é descontado da conta
            extrato += f"Saque: R$ {valor:.2f} | Saldo após saque: R$ {saldo_conta:.2f}\n"
            numero_saques += 1
            print(f"Saque realizado com sucesso! Saldo da conta: R$ {saldo_conta:.2f}")
        else:
            print("Operação falhou! O valor informado é inválido.")

    elif opcao == "e":
        print("\n================ EXTRATO ================")
        if extrato:
            print(extrato)
        else:
            print("Não foram realizadas movimentações.")
        print(f"\nSaldo da conta: R$ {saldo_conta:.2f}")
        print("==========================================")

    elif opcao == "q":
        print("Saindo... Até logo!")
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
