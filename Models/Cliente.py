from Models.Pessoa import Pessoa

class Cliente(Pessoa):
    
    def __init__(self, id_cliente=None, data_registo=None, limite_credito=0.0, **kwargs):
        super().__init__(id_pessoa = id_cliente , **kwargs)
        self.id_cliente = id_cliente
        self.data_registo = data_registo
        self.limite_credito = limite_credito


    def __repr__(self):
        return f"<Cliente: {self.nome} | Telefone: {self.telefone} | Email: {self.email} | Limite Crédito {self.limite_credito}>"