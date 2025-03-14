
usuarios = []
contas = []

proximo_numero_conta = 1



def deposito(saldo, valor, extrato, /):

    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f} | Saldo após depósito: R$ {saldo:.2f}\n"
    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato

def saque(*, saldo, valor, extrato, limite, numero_saques, limite_saques):

    if valor <= 0:
        print("Operação falhou! O valor informado é inválido.")
    elif valor > saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
    elif valor > limite:
        print("Operação falhou! O valor do saque excede o limite.")
    elif numero_saques >= limite_saques:
        print("Operação falhou! Número máximo de saques excedido.")
    else:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f} | Saldo após saque: R$ {saldo:.2f}\n"
        numero_saques += 1
        print(f"Saque realizado com sucesso! Saldo da conta: R$ {saldo:.2f}")
    return saldo, extrato, numero_saques

def exibir_extrato(saldo, /, *, extratos):

    print("\n================ EXTRATO ================")
    if extratos:
        print(extratos)
    else:
        print("Não foram realizadas movimentações.")
    print(f"\nSaldo da conta: R$ {saldo:.2f}")
    print("==========================================")

# Funções de cadastro e criação de contas

def criar_usuario():

    cpf = input("Informe o CPF (somente números): ").strip()
    # Verifica se o CPF já foi cadastrado
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            print("Já existe um usuário com este CPF!")
            return None
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ")
    endereco = input("Informe o endereço: ")
    usuario = {"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco}
    usuarios.append(usuario)
    print("Usuário cadastrado com sucesso!")
    return usuario

def criar_conta_corrente(usuario):
    """
    Cria uma conta corrente vinculada a um usuário.
    Cada conta possui agência fixa '0001', número sequencial, saldo e dados para movimentações.
    """
    global proximo_numero_conta
    if usuario is None:
        print("Usuário inválido. Realize o cadastro do usuário primeiro.")
        return None
    # Conta possui dados para movimentação
    conta = {
        "agencia": "0001",
        "numero_conta": proximo_numero_conta,
        "usuario": usuario,
        "saldo": 0,
        "limite": 500,
        "extrato": "",
        "numero_saques": 0,
        "LIMITE_SAQUES": 3
    }
    contas.append(conta)
    print(f"Conta criada com sucesso! Agência: {conta['agencia']} | Número: {conta['numero_conta']}")
    proximo_numero_conta += 1
    return conta

def listar_contas():
    """
    Lista todas as contas criadas.
    """
    if not contas:
        print("Nenhuma conta cadastrada.")
        return
    for conta in contas:
        usuario = conta["usuario"]
        print(f"Agência: {conta['agencia']} | Conta: {conta['numero_conta']} | Titular: {usuario['nome']} - CPF: {usuario['cpf']}")

def entrar_na_conta():

    cpf = input("Informe o CPF: ").strip()
    conta_encontrada = None
    # Filtra contas vinculadas ao CPF (removendo espaços)
    contas_usuario = [conta for conta in contas if conta["usuario"]["cpf"].strip() == cpf]
    if not contas_usuario:
        print("Nenhuma conta encontrada para esse CPF. Certifique-se de que você cadastrou o usuário e criou a conta!")
        return None
    if len(contas_usuario) == 1:
        conta_encontrada = contas_usuario[0]
    else:
        print("Contas encontradas:")
        for conta in contas_usuario:
            print(f"Conta: {conta['numero_conta']} | Agência: {conta['agencia']}")
        try:
            numero = int(input("Informe o número da conta que deseja acessar: "))
        except ValueError:
            print("Número de conta inválido!")
            return None
        for conta in contas_usuario:
            if conta["numero_conta"] == numero:
                conta_encontrada = conta
                break
        if conta_encontrada is None:
            print("Conta não encontrada.")
    return conta_encontrada

def menu_operacoes(conta):

    while True:
        menu = """
[d] Depositar
[s] Sacar
[e] Extrato
[r] Sair da Conta

=> """
        opcao = input(menu).lower()
        if opcao == "d":
            try:
                valor = float(input("Informe o valor do depósito: "))
            except ValueError:
                print("Valor inválido!")
                continue
            conta["saldo"], conta["extrato"] = deposito(conta["saldo"], valor, conta["extrato"])
            print(f"Depósito realizado com sucesso! Saldo da conta: R$ {conta['saldo']:.2f}")
        elif opcao == "s":
            try:
                valor = float(input("Informe o valor do saque: "))
            except ValueError:
                print("Valor inválido!")
                continue
            conta["saldo"], conta["extrato"], conta["numero_saques"] = saque(
                saldo=conta["saldo"],
                valor=valor,
                extrato=conta["extrato"],
                limite=conta["limite"],
                numero_saques=conta["numero_saques"],
                limite_saques=conta["LIMITE_SAQUES"]
            )
        elif opcao == "e":
            exibir_extrato(conta["saldo"], extratos=conta["extrato"])
        elif opcao == "r":
            print("Saindo da conta...")
            break
        else:
            print("Operação inválida, por favor selecione novamente.")

def main():
    """
    Menu principal do sistema.

    """
    while True:
        menu = """
[cu] Cadastrar Usuário
[cc] Criar Conta Corrente
[lc] Listar Contas
[e] Entrar na Conta
[q] Sair

=> """
        opcao = input(menu).lower()
        if opcao == "cu":
            criar_usuario()
        elif opcao == "cc":
            cpf = input("Informe o CPF do usuário para vincular a conta: ").strip()
            usuario_encontrado = None
            for usuario in usuarios:
                if usuario["cpf"].strip() == cpf:
                    usuario_encontrado = usuario
                    break
            if usuario_encontrado:
                criar_conta_corrente(usuario_encontrado)
            else:
                print("Usuário não encontrado. Cadastre o usuário primeiro.")
        elif opcao == "lc":
            listar_contas()
        elif opcao == "e":
            conta_logada = entrar_na_conta()
            if conta_logada:
                print(f"Bem-vindo, {conta_logada['usuario']['nome']}!")
                menu_operacoes(conta_logada)
        elif opcao == "q":
            print("Saindo... Até logo!")
            break
        else:
            print("Operação inválida, por favor selecione novamente.")

if __name__ == "__main__":
    main()
