class RoleUtilizador:
    def __init__(self, id_role=None, nome=None, descricao=None):
        self.id_role = id_role
        self.nome = nome
        self.descricao = descricao

    def __repr__(self):
        return f"<Role {self.id_role}: {self.nome}>"