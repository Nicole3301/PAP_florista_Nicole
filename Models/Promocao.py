class Promocao:
    def __init__(self, id_promocao=None, nome=None, desconto=0.0, data_inicio=None, data_fim=None):
        self.id_promocao = id_promocao
        self.nome = nome
        self.desconto = desconto
        self.data_inicio = data_inicio
        self.data_fim = data_fim

    def __repr__(self):
        return f"<Promoção {self.id_promocao}: {self.nome}, {self.desconto}%>"