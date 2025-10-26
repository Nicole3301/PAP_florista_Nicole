from Models.Utilizador import Utilizador


class UtilizadorDAL:
    def criarUtilizador(self, utilizador: Utilizador): 
        query_pessoa = """
        INSERT INTO Pessoa (nome, email, telefone, morada, data_nascimento)
        VALUES (%s, %s, %s, %s, %s) RETURNING id_pessoa
        """
        id_pessoa = self.db.retornaDado(query_pessoa, (utilizador.nome, utilizador.email, utilizador.telefone, utilizador.morada, utilizador.data_nascimento))[0]
            
        query_utilizador = """
        INSERT INTO Utilizador (id_utilizador, username, password_hash, ultimo_login, id_role)
        VALUES (%s, %s, %s, %s, %s)
        """
        self.db.executarQuery(query_utilizador, (id_pessoa, utilizador.username, utilizador.password_hash, utilizador.ultimo_login, utilizador.id_role))
        
        query_funcionario = """
        INSERT INTO Funcionario (id_funcionario, cargo, departamento, data_contratacao, salario)
        VALUES (%s, %s, %s, %s, %s)
        """
        self.db.executarQuery(query_funcionario, (id_pessoa, utilizador.cargo, utilizador.departamento, utilizador.data_contratacao, utilizador.salario))    
            
        return id_pessoa
    
    def obterTodosUtilizadores(self):  
        query = """ 
        SELECT u.id_utilizador, u.username, u.password_hash, u.ultimo_login, u.id_role
        FROM utilizador as u 
        ORDER BY u.id_utilizador ASC
        """ 
        rows = self.db.retornaListaDados(query)
        
        return [Utilizador(
            id_utilizador=row[0],
            username=row[1],
            password_hash=row[2],
            ultimo_login=row[3],
            id_role=row[4]
        ) for row in rows]
        
    def obterPessoa(self, id_utilizador):
        query = """ 
        SELECT p.id_pessoa, p.nome, p.email, p.telefone, p.morada, p.data_nascimento
        FROM pessoa as p
        INNER JOIN utilizador as u on p.id_pessoa = u.id_utilizador
        WHERE u.id_utilizador = %s
        """ 
        rows = self.db.retornaListaDados(query, (id_utilizador,))
        
        return [Utilizador(
            id_pessoa=row[0],
            nome=row[1],
            email=row[2],
            telefone=row[3],
            morada=row[4],
            data_nascimento=row[5]
        ) for row in rows]
        
    def atualizarUtilizador(self, utilizador : Utilizador):
        query_utilizador = """
        UPDATE Utilizador
        SET username=%s, password_hash=%s, id_role=%s
        WHERE id_utilizador=%s
        """
        self.db.executaQuery(query_utilizador, (utilizador.username, utilizador.password_hash, utilizador.id_role, utilizador.id_utilizador))
    
    def eliminarUtilizador(self, id_utilizador:int):
        self.db.executaQuery("DELETE FROM Utilizador WHERE id_utilizador=%s", (id_utilizador,))
        self.db.executaQuery("DELETE FROM Pessoa WHERE id_pessoa=%s", (id_utilizador,))
        self.db.executaQuery("DELETE FROM funcionario WHERE id_funcionario=%s", (id_utilizador,))