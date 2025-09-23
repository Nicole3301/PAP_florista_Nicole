class Encomenda:
    def __init__(self, id_encomenda=None, id_cliente=None, data_encomenda=None, estado="pendente"):
        self.id_encomenda = id_encomenda
        self.id_cliente = id_cliente
        self.data_encomenda = data_encomenda
        self.estado = estado

    def __repr__(self):
        return f"<Encomenda {self.id_encomenda}: Cliente {self.id_cliente}, Estado {self.estado}>"