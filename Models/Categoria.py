class CategoriaProduto:
   
    def __init__(self, id_categoria=None, nome=None, descricao=None):
        self.id_categoria = id_categoria
        self.nome = nome
        self.descricao = descricao

    
    def __repr__(self):
        return f"<Categoria {self.id_categoria}: {self.nome}>"