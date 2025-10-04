from Models.Cliente import Cliente

class ClienteDAL:
    def __init__(self, db):
        self.db = db



    def criarCliente(self, cliente: Cliente):
        
        query = """
        INSERT INTO Pessoa (nome, email, telefone, morada, data_nascimento)
        VALUES (%s, %s, %s, %s, %s) RETURNING id_pessoa
        """
        pessoa_id = self.db.retornaDado(query, (cliente.nome, cliente.email, cliente.telefone, cliente.morada, cliente.data_nascimento))[0]


        query_cliente = """
        INSERT INTO Cliente (id_cliente, data_registo)
        VALUES (%s, %s)
        """
        self.db.executaQuery(query_cliente, (pessoa_id, cliente.data_registo))
        return pessoa_id



    def obterTodosClientes(self):
        query = """
        SELECT p.id_pessoa, p.nome, p.email, p.telefone, p.morada, p.data_nascimento,
               c.data_registo
        FROM Cliente c
        INNER JOIN Pessoa p ON c.id_cliente = p.id_pessoa
		ORDER BY p.id_pessoa ASC;
        """
        rows = self.db.retornaListaDados(query)
        
        return [Cliente(
            id_cliente=row[0],
            nome=row[1],
            email=row[2],
            telefone=row[3],
            morada=row[4],
            data_nascimento=row[5],
            data_registo=row[6]
        ) for row in rows]




    def atualizarCliente(self, cliente: Cliente):
        query_pessoa = """
        UPDATE Pessoa
        SET nome=%s, email=%s, telefone=%s, morada=%s
        WHERE id_pessoa=%s
        """
        self.db.executaQuery(query_pessoa, (cliente.nome, cliente.email, cliente.telefone, cliente.morada, cliente.id_cliente))

        query_cliente = """
        UPDATE Cliente
        SET data_registo=%s
        WHERE id_cliente=%s
        """
        self.db.executaQuery(query_cliente, (cliente.data_registo, cliente.id_cliente))



        
    def eliminarCliente (self, id_cliente:int):
        self.db.executaQuery("DELETE FROM Cliente WHERE id_cliente=%s", (id_cliente,))
        self.db.executaQuery("DELETE FROM Pessoa WHERE id_pessoa=%s", (id_cliente,))