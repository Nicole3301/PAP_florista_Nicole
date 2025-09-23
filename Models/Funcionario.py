from Models.Pessoa import Pessoa

class Funcionario(Pessoa):
    def __init__(self, id_funcionario=None, cargo=None, departamento=None, salario=0.0, data_contratacao=None, **kwargs):
        super().__init__(id_pessoa=id_funcionario, **kwargs)
        self.id_funcionario = id_funcionario
        self.cargo = cargo
        self.departamento = departamento
        self.salario = salario
        self.data_contratacao = data_contratacao

    def __repr__(self):
        return f"<Funcionario {self.id_funcionario}: {self.nome}, Cargo {self.cargo}>"