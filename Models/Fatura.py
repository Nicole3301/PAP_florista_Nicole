class Fatura:
    def __init__(self, id_fatura=None, id_encomenda=None, data_emissao=None, valor_total=0.0):
        self.id_fatura = id_fatura
        self.id_encomenda = id_encomenda
        self.data_emissao = data_emissao
        self.valor_total = valor_total

    def __repr__(self):
        return f"<Fatura {self.id_fatura}: Encomenda {self.id_encomenda}, Total {self.valor_total}€>"