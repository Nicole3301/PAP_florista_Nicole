class Produto:
    def __init__(self, id_produto=None, nome=None, preco=0.0, stock=0, quantidade=0, id_categoria=None):
        self.id_produto = id_produto
        self.nome = nome
        self.preco = preco
        self.stock = stock
        self.quantidade = quantidade
        self.id_categoria = id_categoria

    def __repr__(self):
        return f"<Produto {self.id_produto}: {self.nome}, {self.preco}€, stock {self.stock}>"