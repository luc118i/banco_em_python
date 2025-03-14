from abc import ABC, abstractmethod
from datetime import date

# Definição das classes conforme o UML

class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta) -> bool:
        pass

class Historico:
    def __init__(self):
        self._transacoes = []
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(transacao)
    
    @property
    def transacoes(self):
        return self._transacoes

class Conta:
    def __init__(self, cliente, numero, agencia='0001'):
        self._saldo = 0.0
        self._numero = numero
        self._agencia = agencia
        self._cliente = cliente
        self._historico = Historico()
    
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(cliente, numero)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def depositar(self, valor) -> bool:
        if valor > 0:
            self._saldo += valor
            return True
        else:
            return False
    
    def sacar(self, valor) -> bool:
        if valor > 0 and valor <= self._saldo:
            self._saldo -= valor
            return True
        return False

class ContaCorrente(Conta):
    def __init__(self, cliente, numero, agencia='0001', limite=500, limite_saques=3):
        super().__init__(cliente, numero, agencia)
        self._limite = limite
        self._limite_saques = limite_saques
        self._numero_saques = 0
    
    def sacar(self, valor) -> bool:
        excedeu_valor = valor > self._limite
        excedeu_saldo = valor > self._saldo
        excedeu_saques = self._numero_saques >= self._limite_saques
        
        if excedeu_valor:
            print("Operação falhou! O valor do saque excede o limite.")
            return False
        elif excedeu_saldo:
            print("Operação falhou! Saldo insuficiente.")
            return False
        elif excedeu_saques:
            print("Operação falhou! Número máximo de saques excedido.")
            return False
        elif valor <= 0:
            print("Operação falhou! Valor inválido.")
            return False
        else:
            self._saldo -= valor
            self._numero_saques += 1
            return True

class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []
    
    def realizar_transacao(self, conta, transacao):
        return transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
        self._contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento
    
    @property
    def cpf(self):
        return self._cpf
    
    @property
    def nome(self):
        return self._nome
    
    @property
    def data_nascimento(self):
        return self._data_nascimento

# Implementação das funções do sistema

usuarios = []
contas = []
proximo_numero_conta = 1

def criar_usuario():
    cpf = input("Informe o CPF (somente números): ").strip()
    for usuario in usuarios:
        if usuario.cpf == cpf:
            print("Já existe um usuário com este CPF!")
            return None
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ")
    endereco = input("Informe o endereço: ")
    usuario = PessoaFisica(cpf, nome, data_nascimento, endereco)
    usuarios.append(usuario)
    print("Usuário cadastrado com sucesso!")
    return usuario

def criar_conta_corrente(usuario):
    global proximo_numero_conta
    if not usuario:
        print("Usuário inválido.")
        return None
    conta = ContaCorrente(usuario, proximo_numero_conta)
    usuario.adicionar_conta(conta)
    contas.append(conta)
    proximo_numero_conta += 1
    print(f"Conta criada com sucesso! Agência: {conta.agencia} | Número: {conta.numero}")
    return conta

def listar_contas():
    if not contas:
        print("Nenhuma conta cadastrada.")
        return
    for conta in contas:
        print(f"Agência: {conta.agencia} | Conta: {conta.numero} | Titular: {conta.cliente.nome} - CPF: {conta.cliente.cpf}")

def entrar_na_conta():
    cpf = input("Informe o CPF: ").strip()
    contas_usuario = [conta for conta in contas if conta.cliente.cpf == cpf]
    if not contas_usuario:
        print("Nenhuma conta encontrada para este CPF.")
        return None
    if len(contas_usuario) == 1:
        return contas_usuario[0]
    else:
        print("Contas encontradas:")
        for conta in contas_usuario:
            print(f"Conta: {conta.numero} | Agência: {conta.agencia}")
        try:
            numero = int(input("Informe o número da conta: "))
        except ValueError:
            print("Número inválido.")
            return None
        for conta in contas_usuario:
            if conta.numero == numero:
                return conta
        print("Conta não encontrada.")
        return None

def exibir_extrato(conta):
    print("\n================ EXTRATO ================")
    if not conta.historico.transacoes:
        print("Não foram realizadas movimentações.")
    else:
        for transacao in conta.historico.transacoes:
            if isinstance(transacao, Deposito):
                print(f"Depósito: R$ {transacao.valor:.2f}")
            elif isinstance(transacao, Saque):
                print(f"Saque: R$ {transacao.valor:.2f}")
    print(f"\nSaldo atual: R$ {conta.saldo:.2f}")
    print("==========================================")

class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor
    
    def registrar(self, conta) -> bool:
        sucesso = conta.depositar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)
            print(f"Depósito de R$ {self.valor:.2f} realizado. Saldo atual: R$ {conta.saldo:.2f}")
        else:
            print("Operação falhou! Valor de depósito inválido.")
        return sucesso

class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor
    
    def registrar(self, conta) -> bool:
        sucesso = conta.sacar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)
            print(f"Saque de R$ {self.valor:.2f} realizado. Saldo atual: R$ {conta.saldo:.2f}")
        else:
            print("Operação falhou! Não foi possível realizar o saque.")
        return sucesso

def menu_operacoes(conta):
    cliente = conta.cliente
    while True:
        opcao = input("\n[d] Depositar\n[s] Sacar\n[e] Extrato\n[r] Sair\n=> ").lower()
        if opcao == 'd':
            try:
                valor = float(input("Valor do depósito: "))
                transacao = Deposito(valor)
                cliente.realizar_transacao(conta, transacao)
            except ValueError:
                print("Valor inválido.")
        elif opcao == 's':
            try:
                valor = float(input("Valor do saque: "))
                transacao = Saque(valor)
                cliente.realizar_transacao(conta, transacao)
            except ValueError:
                print("Valor inválido.")
        elif opcao == 'e':
            exibir_extrato(conta)
        elif opcao == 'r':
            print("Saindo da conta...")
            break
        else:
            print("Opção inválida.")

def main():
    while True:
        opcao = input("\n[cu] Cadastrar Usuário\n[cc] Criar Conta\n[lc] Listar Contas\n[e] Entrar\n[q] Sair\n=> ").lower()
        if opcao == 'cu':
            criar_usuario()
        elif opcao == 'cc':
            cpf = input("CPF do usuário: ").strip()
            usuario = next((u for u in usuarios if u.cpf == cpf), None)
            if usuario:
                criar_conta_corrente(usuario)
            else:
                print("Usuário não encontrado.")
        elif opcao == 'lc':
            listar_contas()
        elif opcao == 'e':
            conta = entrar_na_conta()
            if conta:
                print(f"Bem-vindo(a), {conta.cliente.nome}!")
                menu_operacoes(conta)
        elif opcao == 'q':
            print("Saindo...")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()