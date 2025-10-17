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

        query_update_stock=""" 
        UPDATE Produto 
        SET stock = stock - %s 
        WHERE id_produto = %s
        """
        self.db.executaQuery(query_update_stock,(produto.quantidade, produto.id_produto))

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
        
    def obterTodosProdutos(self, id_encomenda):
        query = """
        SELECT ep.id_produto, p.nome, ep.quantidade, p.preco
        FROM encomenda_produto ep
        INNER JOIN Produto p ON ep.id_produto = p.id_produto
		WHERE ep.id_encomenda = %s
        """ 
        rows = self.db.retornaListaDados(query, (id_encomenda,))
 
        return [Produto(
            id_produto=row[0],
            nome=row[1],
            quantidade=row[2],
            preco=row[3]
        ) for row in rows]
        
   
    def atualizarPromocao(self, promocao: Promocao):
        query = """
        UPDATE Promocao
        SET nome=%s, desconto=%s, data_inicio=%s, data_fim=%s
        WHERE id_promocao=%s
        """
        self.db.executaQuery(query, (promocao.nome, promocao.desconto, promocao.data_inicio, promocao.data_fim))
        
    def eliminarEncomenda(self, id_promocao:int):
        self.db.executaQuery("DELETE FROM Produto_encomenda WHERE id_promocao=%s", (id_promocao,)) 
        self.db.executaQuery("DELETE FROM Promocao WHERE id_encomenda=%s", (id_promocao,)) 
