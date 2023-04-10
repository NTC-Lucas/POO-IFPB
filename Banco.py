import re
from abc import ABC, abstractmethod

class SaqueNegado(Exception):
    pass


class LimiteChequeEspecialExcedente(Exception):
    pass


class ContaBancaria(ABC):
    def __init__(self, nome, numero, saldo):
        self._numero = None
        self.numero = numero
        self._saldo = saldo
        self._nome = nome

    @property
    def numero(self):
        return self._numero

    @numero.setter
    def numero(self, numero):
        assert isinstance(numero, str), "Número da conta deve ser uma string"
        assert len(numero) <= 7, "Número da conta deve ter no máximo 7 caracteres"
        assert re.match(r'^\d{5}-\w$', numero), "Número da conta deve ser formado por 5 dígitos, seguido de hífen e um dígito ou letra X"
        self._numero = numero

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nome):
        assert isinstance(nome, str), "Nome deve ser uma string"
        self._nome = nome

    @property
    def saldo(self):
        return self._saldo

    @saldo.setter
    def saldo(self, saldo):
        assert isinstance(saldo, (int, float)), "O saldo da conta deve ser um valor numérico."
        self._saldo = saldo

    def depositar(self, valor_depositado):
        assert isinstance(valor_depositado, (int, float)), "Valor depositado deve ser um número"
        self._saldo += valor_depositado

    @abstractmethod
    def verificar_saldo_disponivel(self, valor_saque):
        pass

    def sacar(self, valor_sacar):
        if self.verificar_saldo_disponivel(valor_sacar):
            self._saldo -= valor_sacar
        else:
            raise SaqueNegado(
                "Valor a sacar precisa ser menor ou igual ao saldo da conta somado ao limite do cheque especial.")

    def __str__(self):
        return f'''Nome da conta: {self._nome}\nNumero da conta: {self._numero}\nSaldo da conta: {self._saldo}'''


class ContaPoupanca(ContaBancaria):
    def __init__(self, nome, numero, saldo, taxa_juros):
        super().__init__(nome, numero, saldo)
        self.taxa_juros = taxa_juros

    @property
    def taxa_juros(self):
        return self._taxa_juros

    @taxa_juros.setter
    def taxa_juros(self, taxa_juros):
        assert isinstance(taxa_juros, (float, int)), "A taxa de juros deve ser um número real"
        assert 0 <= taxa_juros <= 1, "A taxa de juros deve ser um número entre 0 e 1"
        self._taxa_juros = taxa_juros

    def calcular_taxa_anual(self):
        return self._saldo * self._taxa_juros

    def verificar_saldo_disponivel(self, valor_saque):
        return self._saldo >= valor_saque

    def __str__(self):
        return f'{super().__str__()}\nJuros anual é de: {self.calcular_taxa_anual()}\n'


class ContaCorrente(ContaBancaria):
    _limite_cheque_especial_maximo = 1000

    def __init__(self, nome, numero, saldo, limite_cheque_especial=_limite_cheque_especial_maximo):
        super().__init__(nome, numero, saldo)
        assert isinstance(limite_cheque_especial, (int, float)) and limite_cheque_especial >= 0, "O limite do cheque especial deve ser um valor numérico positivo."
        assert limite_cheque_especial <= self._limite_cheque_especial_maximo, f"O limite do cheque especial não pode ser maior do que {self._limite_cheque_especial_maximo}"
        self.limite_cheque_especial = limite_cheque_especial

    @classmethod
    def limite_cheque_especial_maximo(cls):
        return cls._limite_cheque_especial_maximo

    @property
    def limite_cheque_especial(self):
        return self._limite_cheque_especial

    @limite_cheque_especial.setter
    def limite_cheque_especial(self, valor):
        assert isinstance(valor, (int, float)) and valor >= 0, "O limite do cheque especial deve ser um valor numérico positivo."
        assert valor <= self._limite_cheque_especial_maximo, f"O limite do cheque especial não pode ser maior do que {self._limite_cheque_especial_maximo}"
        self._limite_cheque_especial = valor

    def verificar_saldo_disponivel(self, valor_saque):
        return self._saldo + self._limite_cheque_especial >= valor_saque

    def sacar(self, valor_sacar):
        if valor_sacar <= self._saldo:
            self._saldo -= valor_sacar
        elif valor_sacar <= self._saldo + self._limite_cheque_especial:
            self._limite_cheque_especial -= (valor_sacar - self._saldo)
            self._saldo = 0
        else:
            raise LimiteChequeEspecialExcedente(
                "Valor a sacar precisa ser menor ou igual ao saldo da conta somado ao limite do cheque especial.")

    def __str__(self):
        return f'{super().__str__()}\nLimite do Cheque Especial: {self._limite_cheque_especial}\n'


class ContaInvestimento(ContaBancaria):
    def __init__(self, nome, numero, saldo, taxa_rendimento):
        super().__init__(nome, numero, saldo)
        self.taxa_rendimento = taxa_rendimento

    @property
    def taxa_rendimento(self):
        return self._taxa_rendimento

    @taxa_rendimento.setter
    def taxa_rendimento(self, taxa_rendimento):
        assert isinstance(taxa_rendimento, (float, int)), "A taxa de rendimento deve ser um número real"
        assert 0 <= taxa_rendimento <= 1, "A taxa de rendimento deve ser um número entre 0 e 1"
        self._taxa_rendimento = taxa_rendimento

    def calcular_rentabilidade(self):
        return self._saldo * self._taxa_rendimento

    def verificar_saldo_disponivel(self, valor_saque):
        return self._saldo >= valor_saque

    def __str__(self):
        return f'{super().__str__()}\nRentabilidade anual é de: {self.calcular_rentabilidade()}'


if __name__ == "__main__":
    try:

        corrente = ContaCorrente('Lucas', "12344-X", 500, 1000)
        corrente.sacar(900)
        corrente.depositar(200)
        print(corrente)

        poupanca = ContaPoupanca('Vinicius', "12345-6", 3, 0.5)
        poupanca.depositar(100)
        poupanca.sacar(2)
        print(poupanca)

        investimento = ContaInvestimento('Barbosa', '12345-9', 200, 0.75)
        investimento.depositar(100)
        investimento.sacar(200)
        print(investimento)

    except (AssertionError, ValueError, TypeError, LimiteChequeEspecialExcedente, SaqueNegado) as e:
        print(e)
