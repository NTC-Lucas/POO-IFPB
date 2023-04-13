from abc import ABC, abstractmethod

class Pessoa(ABC):
    def __init__(self, nome='', endereco='', telefone=''):
        self._nome = nome
        self._endereco = endereco
        self._telefone = telefone

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nome):
        assert type(nome) is str, "O nome deve ser uma string."
        self._nome = nome

    @property
    def endereco(self):
        return self._endereco

    @endereco.setter
    def endereco(self, cep):
        assert type(cep) is str, "O endereço deve ser uma string."
        self._endereco = cep

    @property
    def telefone(self):
        return self._telefone

    @telefone.setter
    def telefone(self, numero):
        assert type(numero) is str, "O número deve ser uma string."
        self._telefone = numero

    @abstractmethod
    def calcularSalario(self):
        pass

    def __str__(self):
        return f'''nome {self._nome} \nendereço {self._endereco}\ntelefone{self._telefone}'''


class Fornecedor(Pessoa):
    def __init__(self, nome, endereco, telefone, valorCredito, valorDivida):
        super().__init__(nome, endereco, telefone)
        self._valorCredito = valorCredito
        self._valorDivida = valorDivida

    @property
    def valorCredito(self):
        return self._valorCredito

    @valorCredito.setter
    def valorCredito(self, credito):
        self._valorCredito = credito

    @property
    def valorDivida(self):
        return self._valorDivida

    @valorDivida.setter
    def valorDivida(self, divida):
        self._valorDivida = divida

    def calcularSalario(self):
        pass

    def obterSaldo( self):
        return self._valorCredito - self._valorDivida

    def __str__(self):
        return f'{super().__str__()}\nSaldo = {self.obterSaldo()}'


class Empregado(Pessoa):
    def __init__(self, nome, endereco, telefone, codigoSetor, salarioBase, imposto):
        super().__init__(nome, endereco, telefone)
        self._codigoSetor = codigoSetor
        self._salarioBase = salarioBase
        self._imposto = imposto

    @property
    def codigoSetor(self):
        return self._codigoSetor

    @codigoSetor.setter
    def codigoSetor(self, codigo):
        self._codigoSetor = codigo

    @property
    def salarioBase(self):
        return self._salarioBase

    @salarioBase.setter
    def salarioBase(self, salario):
        self._salarioBase = salario

    @property
    def imposto(self):
        return self._imposto

    @imposto.setter
    def imposto(self, imposto):
        self._imposto = imposto

    def calcularSalario(self):
        return self._salarioBase - (self._salarioBase * (self._imposto / 100))

    def __str__(self):
        return f'{super().__str__()}\nCódigo do setor: {self._codigoSetor}\nSalário base: {self._salarioBase}\nImposto: {self._imposto}%\nSalário líquido: {self.calcularSalario()}'


class Administrador(Empregado):
    def __init__(self, nome, endereco, telefone, codigoSetor, salarioBase, imposto, ajudaDeCusto):
        super().__init__(nome, endereco, telefone, codigoSetor, salarioBase, imposto)
        self._ajudaDeCusto = ajudaDeCusto

    @property
    def ajudaDeCusto(self):
        return self._ajudaDeCusto

    @ajudaDeCusto.setter
    def ajudaDeCusto(self, ajudaDeCusto):
        self._ajudaDeCusto = ajudaDeCusto

    def calcularSalario(self):
        return super().calcularSalario() + self._ajudaDeCusto

    def __str__(self):
        return f'{super().__str__()}\nAjuda de Custo: R${self._ajudaDeCusto:.2f}'

class Operario(Empregado):
    def __init__(self, nome, endereco, telefone, codigoSetor, salarioBase, imposto, valorProducao, comissao):
        super().__init__(nome, endereco, telefone, codigoSetor, salarioBase, imposto)
        self._valorProducao = valorProducao
        self._comissao = comissao

    @property
    def valorProducao(self):
        return self._valorProducao

    @valorProducao.setter
    def valorProducao(self, valor):
        self._valorProducao = valor

    @property
    def comissao(self):
        return self._comissao

    @comissao.setter
    def comissao(self, valor):
        self._comissao = valor

    def calcularSalario(self):
        salario = self._salarioBase + (self._valorProducao * self._comissao)
        return salario

class Vendedor(Empregado):
    def __init__(self, nome='', endereco='', telefone='', codigoSetor=0, salarioBase=0.0, imposto=0.0, valorVendas=0.0, comissao=0.0):
        super().__init__(nome, endereco, telefone, codigoSetor, salarioBase, imposto)
        self._valorVendas = valorVendas
        self._comissao = comissao

    @property
    def valorVendas(self):
        return self._valorVendas

    @valorVendas.setter
    def valorVendas(self, valor):
        self._valorVendas = valor

    @property
    def comissao(self):
        return self._comissao

    @comissao.setter
    def comissao(self, valor):
        self._comissao = valor

    def calcularSalario(self):
        salario = self._salarioBase + (self._valorVendas * self.comissao)
        return salario

    def obterSaldo(self):
        return 0

    def __str__(self):
        return f'{super().__str__()}\nValor de vendas: {self._valorVendas}\nComissão: {self._comissao}\nSalário: {self.calcularSalario()}'


class PessoaFisica(Pessoa):
    def __init__(self, nome='', endereco='', telefone='', cpf='', idade=0):
        super().__init__(nome, endereco, telefone)
        self._cpf = cpf
        self._idade = idade

    @property
    def cpf(self):
        return self._cpf

    @cpf.setter
    def cpf(self, cpf):
        assert type(cpf) is str, "O CPF deve ser uma string."
        self._cpf = cpf

    @property
    def idade(self):
        return self._idade

    @idade.setter
    def idade(self, idade):
        assert type(idade) is int, "A idade deve ser um número inteiro."
        self._idade = idade

    def __str__(self):
        return f'{super().__str__()}\nCPF: {self._cpf}\nIdade: {self._idade}'


class PessoaJuridica(Pessoa):
    def __init__(self, nome='', endereco='', telefone='', cnpj='', inscricaoEstadual=''):
        super().__init__(nome, endereco, telefone)
        self._cnpj = cnpj
        self._inscricaoEstadual = inscricaoEstadual

    @property
    def cnpj(self):
        return self._cnpj

    @cnpj.setter
    def cnpj(self, cnpj):
        assert type(cnpj) is str, "O CNPJ deve ser uma string."
        self._cnpj = cnpj

    @property
    def inscricaoEstadual(self):
        return self._inscricaoEstadual

    @inscricaoEstadual.setter
    def inscricaoEstadual(self, inscricaoEstadual):
        assert type(inscricaoEstadual) is str, "A Inscrição Estadual deve ser uma string."
        self._inscricaoEstadual = inscricaoEstadual

    def __str__(self):
        return f'{super().__str__()}\nCNPJ: {self._cnpj}\nInscrição Estadual: {self._inscricaoEstadual}'


if __name__ == '__main__':
    fornecedor = Fornecedor("João", 30, 2000, 1000, 3000)
    operario = Operario("Maria", 25, 1800, 5000, 0.05, 1209, 12312, 121321)
    vendedor = Vendedor("Pedro", 35, 2200, 6000, 0.04)

    pessoas = []

    pessoas.append(fornecedor)
    pessoas.append(operario)
    pessoas.append(vendedor)

    for pessoa in pessoas:
        print(pessoa.calcularSalario())
        if isinstance(pessoa, Fornecedor):
            print(pessoa.obterSaldo())
        elif isinstance(pessoa, Vendedor):
            print(pessoa.obterSaldo())
