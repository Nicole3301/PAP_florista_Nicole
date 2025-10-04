from Models.Categoria import CategoriaProduto

class CategoriaDAL:
    def __init__(self, db):
        self.db = db

    def criarCategoria(self, categoria: CategoriaProduto):
        query = """
        INSERT INTO Categoria_produto (nome, descricao)
        VALUES (%s, %s) RETURNING id_categoria
        """
        id_categoria = self.db.retornaDado(query, (categoria.nome, categoria.descricao))[0]
        return id_categoria

    def obterTodasCategorias(self):
        query = """
        SELECT id_categoria, nome, descricao 
        FROM categoria_produto
        ORDER BY id_categoria ASC
        """
        rows = self.db.retornaListaDados(query)
        
        return [CategoriaProduto(
            id_categoria=row[0],
            nome=row[1],
            descricao=row[2]
        ) for row in rows]

    def atualizar_categoria(self, categoria: CategoriaProduto):
        query = """
        UPDATE categoria_produto
        SET nome=%s, descricao=%s
        WHERE id_categoria=%s
        """
        self.db.executaQuery(query, (categoria.nome, categoria.descricao, categoria.id_categoria))

        
    def eliminarCategoria(self, id_categoria:int):
        self.db.executaQuery("DELETE FROM Categoria_produto WHERE id_categoria=%s", (id_categoria,))