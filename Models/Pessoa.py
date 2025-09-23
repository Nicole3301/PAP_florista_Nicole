class Pessoa:
    
    def __init__(self, id_pessoa=None, nome=None, email=None, telefone=None, morada=None, data_nascimento=None):
        self.id_pessoa = id_pessoa
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.morada = morada
        self.data_nascimento = data_nascimento

    def __repr__(self):
        return f"<Pessoa : {self.nome}>"