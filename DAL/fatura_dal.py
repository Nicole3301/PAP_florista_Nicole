from Models.Encomenda import Encomenda
from Models.Fatura import Fatura

class FaturaDAL:
    def __init__(self, db):
        self.db = db

    def criarFatura(self, fatura: Fatura):
            
        query = """
        INSERT INTO Fatura (id_encomenda, data_emissao, valor_total)
        VALUES (%s, %s, %s) RETURNING id_fatura
        """
        id_fatura = self.db.retornaDado(query, (fatura.id_encomenda, fatura.data_emissao, fatura.valor_total))[0]
            
        return id_fatura

    def obterTodasFaturas(self):
        query = """
        SELECT f.id_fatura, f.id_encomenda, f.data_emissao, f.valor_total 
        FROM fatura AS f 
        ORDER BY f.data_emissao
        """
        rows = self.db.retornaListaDados(query)
        
        return [Fatura(
            id_fatura=row[0],
            id_encomenda=row[1],
            data_emissao=row[2],
            valor_total=row[3]
        ) for row in rows]
        
    def obterProdutosEncomenda(self, id_encomenda):
        query = """
        SELECT p.id_produto, p.nome, ep.quantidade, p.preco, ep.preco_total
        FROM Encomenda_produto ep
        INNER JOIN Produto p ON ep.id_produto = p.id_produto
        WHERE ep.id_encomenda = %s
        """
        rows = self.db.retornaListaDados(query, (id_encomenda,))
        
        return [Fatura( 
            id_produto=row[0],
            nome=row[1],
            quantidade=row[2],
            preco=row[3],
            preco_total=row[4]
        ) for row in rows]

