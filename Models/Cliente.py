from Models.Pessoa import Pessoa

class Cliente(Pessoa):
    
    def __init__(self, id_cliente=None, data_registo=None, **kwargs):
        super().__init__(id_pessoa = id_cliente , **kwargs)
        self.id_cliente = id_cliente
        self.data_registo = data_registo


    def __repr__(self):
        return f"<Cliente: {self.nome} | Telefone: {self.telefone} | Email: {self.email}>"