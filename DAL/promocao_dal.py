from Models.Promocao import Promocao
from Models.Produto import Produto

class PromocaoDAL:
    def __init__(self, db):
        self.db = db

    def criarPromocao(self, promocao: Promocao):
            
        query = """
        INSERT INTO Promocao (nome, desconto, data_inicio, data_fim)
        VALUES (%s, %s, %s, %s) RETURNING id_promocao
        """
        id_promocao = self.db.retornaDado(query, (promocao.nome, promocao.desconto, promocao.data_inicio, promocao.data_fim))[0]
            
        return id_promocao

    def criarPromocaoProdutos(self, produto: Produto):
       
        query_produto_promocao= """ 
        INSERT INTO Produto_promocao (id_produto, id_promocao)
        VALUES (%s, %s) 
        """
        self.db.executaQuery(query_produto_promocao, (produto.id_produto, produto.id_promocao))

    def obterTodasPromocoes(self):
        query = """
        SELECT p.id_promocao, p.nome, p.desconto, p.data_inicio, p.data_fim
        FROM Promocao AS p 
        ORDER BY p.data_inicio ASC
        """
        rows = self.db.retornaListaDados(query)
        
        return [Promocao(
            id_promocao=row[0],
            nome=row[1],
            desconto=row[2],
            data_inicio=row[3],
            data_fim=row[4]
        ) for row in rows]
  
    def verificar_promocao(self):
 
        query = """
        SELECT  ep.id_produto, p.nome, e.data_encomenda, ep.quantidade, p.preco, pr.desconto, ep.preco_total 
        FROM encomenda AS e 
        INNER JOIN encomenda_produto AS ep ON e.id_encomenda = ep.id_encomenda 
        INNER JOIN Produto AS p ON ep.id_produto = p.id_produto 
        INNER JOIN Produto_promocao AS pp ON p.id_produto = pp.id_produto
        INNER JOIN Promocao AS pr ON pp.id_promocao = pr.id_promocao
        WHERE e.data_encomenda BETWEEN pr.data_inicio AND pr.data_fim
        ORDER BY e.data_encomenda DESC
        LIMIT 1
        """
        return self.db.retornaListaDados(query)
    
    
   
    def atualizarPromocao(self, promocao: Promocao):
        query = """
        UPDATE Promocao
        SET nome=%s, desconto=%s, data_inicio=%s, data_fim=%s
        WHERE id_promocao=%s
        """
        self.db.executaQuery(query, (promocao.nome, promocao.desconto, promocao.data_inicio, promocao.data_fim, promocao.id_promocao))
        
    def eliminarEncomenda(self, id_promocao:int):
        self.db.executaQuery("DELETE FROM Produto_encomenda WHERE id_promocao=%s", (id_promocao,)) 
        self.db.executaQuery("DELETE FROM Promocao WHERE id_promocao=%s", (id_promocao,)) 
