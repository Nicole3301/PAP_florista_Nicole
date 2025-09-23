from Models.Pessoa import Pessoa

class Utilizador(Pessoa):
    def __init__(self, id_utilizador=None, username=None, password_hash=None, ultimo_login=None, id_role=None, **kwargs):
        super().__init__(id_pessoa=id_utilizador, **kwargs)
        self.id_utilizador = id_utilizador
        self.username = username
        self.password_hash = password_hash
        self.ultimo_login = ultimo_login
        self.id_role = id_role

    def __repr__(self):
        return f"<Utilizador {self.id_utilizador}: {self.username}, Role {self.id_role}>"