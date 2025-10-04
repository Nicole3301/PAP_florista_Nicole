from Models.Encomenda import Encomenda
from Models.Produto import Produto

class EncomendaDAL:
    def __init__(self, db):
        self.db = db

    def criarEncomenda(self, encomenda: Encomenda, produto: Produto):
        
        query = """
        INSERT INTO Encomenda (id_cliente, estado)
        VALUES (%s, %s) RETURNING id_encomenda
        """
        id_encomenda = self.db.retornaDado(query, (encomenda.id_cliente, encomenda.estado))[0]
        
        query_encomenda_produto    = """ 
        INSERT INTO Encomenda_produto (id_encomenda, id_produto, quantidade)
        VALUES (%s, %s, %s) 
        """
        self.db.executaQuery(query_encomenda_produto, (id_encomenda, produto.id_produto, produto.quantidade))

        query_update_stock=""" 
        UPDATE Produto SET stock = stock - %s WHERE id_produto = %s
        """
        self.db.executaQuery(query_update_stock,(produto.quantidade, produto.id_produto))
            
        return id_encomenda  

    def obterTodasEncomendas(self):
        query = """
		SELECT e.id_encomenda, e.id_cliente, p.nome, e.data_encomenda, e.estado
		FROM Encomenda AS e 
		INNER JOIN Pessoa AS p ON e.id_cliente = p.id_pessoa 
		ORDER BY e.id_encomenda ASC
        """
        rows = self.db.retornaListaDados(query)
        
        return [Encomenda(
            id_encomenda=row[0],
            id_cliente=row[1],
            data_encomenda=row[2],
            estado=row[3]
        ) for row in rows]
    
    def obterTodosProdutos(self, id_encomenda):
        query = """
        SELECT p.id_produto, p.nome, ep.quantidade, p.preco, ep.preco_total
        FROM encomenda_produto ep
        INNER JOIN Produto p ON ep.id_produto = p.id_produto
		WHERE ep.id_encomenda = %s
        """
        rows = self.db.retornaListaDados(query, (id_encomenda,))
        
        return [Produto(
            id_produto=row[0],
            nome=row[1],
            quantidade=row[2],
            preco=row[3],
            preco_total=[4]
        ) for row in rows]

    def atualizarEncomenda(self, encomenda: Encomenda):
        query = """
        UPDATE Encomenda
        SET estado=%s   
        WHERE id_encomenda=%s
        """
        self.db.executaQuery(query, (encomenda.estado, encomenda.id_encomenda))
        
    def eliminarEncomenda(self, id_encomenda:int):
        self.db.executaQuery("DELETE FROM Encomenda_produto WHERE id_encomenda=%s", (id_encomenda,)) # apaga os produtos que estao ligados a encomenda
        self.db.executaQuery("DELETE FROM Encomenda WHERE id_encomenda=%s", (id_encomenda,)) # apaga a encomenda 
