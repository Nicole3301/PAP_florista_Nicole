from Models.Produto import Produto

class ProdutoDAL:
    def __init__(self, db):
        self.db = db

    def criarProduto(self, produto: Produto):
        query = """
        INSERT INTO Produto (nome, preco, stock, id_categoria)
        VALUES (%s, %s, %s, %s) RETURNING id_produto
        """
        id_produto = self.db.retornaDado(query, (produto.nome, produto.preco, produto.stock, produto.id_categoria))[0]
        return id_produto

    def obterTodosProdutos(self):
        query = """
        SELECT id_produto, p.nome, p.preco, p.stock, c.nome AS categoria_nome
        FROM produto p
        INNER JOIN Categoria_produto c ON p.id_categoria = c.id_categoria
        ORDER BY id_produto ASC
        """
        rows = self.db.retornaListaDados(query)
        
        return [Produto(
            id_produto=row[0],
            nome=row[1],
            preco=row[2],
            stock=row[3],
            id_categoria=row[4]
        ) for row in rows]

    def atualizar_produto(self, produto: Produto):
        query = """
        UPDATE Produto
        SET nome=%s, preco=%s, stock=%s, id_categoria=%s
        WHERE id_produto=%s
        """
        self.db.executaQuery(query, (produto.nome, produto.preco, produto.stock, produto.id_categoria, produto.id_produto))

        
    def eliminarProduto (self, id_produto:int):
        self.db.executaQuery("DELETE FROM Produto WHERE id_produto=%s", (id_produto,))