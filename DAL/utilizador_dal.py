from Models.Utilizador import Utilizador
from Models.RoleUtilizador import RoleUtilizador
from Models.Funcionario import Funcionario
import datetime


class UtilizadorDAL:
    def __init__(self, db):
        self.db = db
    
    def criarUtilizador(self, utilizador: Utilizador, funcionario: Funcionario): 
        query_pessoa = """
        INSERT INTO Pessoa (nome, email, telefone, morada, data_nascimento)
        VALUES (%s, %s, %s, %s, %s) RETURNING id_pessoa
        """
        id_pessoa = self.db.retornaDado(query_pessoa, (utilizador.nome, utilizador.email, utilizador.telefone, utilizador.morada, utilizador.data_nascimento))[0]
            
        query_utilizador = """
        INSERT INTO Utilizador (id_utilizador, username, password_hash, ultimo_login, id_role)
        VALUES (%s, %s, %s, %s, %s)
        """
        self.db.executaQuery(query_utilizador, (id_pessoa, utilizador.username, utilizador.password_hash, datetime.datetime.now(), utilizador.id_role))
        
        query_funcionario = """
        INSERT INTO Funcionario (id_funcionario, cargo, departamento, data_contratacao, salario)
        VALUES (%s, %s, %s, %s, %s)
        """
        self.db.executaQuery(query_funcionario, (id_pessoa, funcionario.cargo, funcionario.departamento, funcionario.data_contratacao, funcionario.salario))    
        
        print("DEBUG FUNCIONARIO:", id_pessoa, funcionario.cargo, funcionario.departamento, funcionario.data_contratacao, funcionario.salario)

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
        
    def obterTodosFuncionarios(self, id_funcionario):
        query = """ 
        SELECT f.cargo, f.departamento, f.data_contratacao, f.salario
        FROM funcionario as f
        INNER JOIN pessoa as p on p.id_pessoa = f.id_funcionario
        WHERE id_funcionario = %s
        """ 
        rows = self.db.retornaListaDados(query, (id_funcionario,))
        
        return [Funcionario(
            cargo=row[0],
            departamento=row[1],
            data_contratacao=row[2],
            salario=row[3]
        ) for row in rows]  
        
        
    def obterTodosFuncionarioComUtilizadores(self):
        query_utilizadores = """ 
        SELECT p.id_pessoa, p.nome, p.email, p.telefone, p.morada, p.data_nascimento, u.username, u.password_hash, ru.nome, f.cargo, f.departamento, f.data_contratacao, f.salario
        FROM utilizador as u
        LEFT JOIN pessoa as p ON u.id_utilizador = p.id_pessoa
        LEFT JOIN funcionario as f ON  f.id_funcionario = p.id_pessoa
        LEFT JOIN role_utilizador as ru ON ru.id_role = u.id_role      
        ORDER BY p.id_pessoa ASC
        """ 
        return  self.db.retornaListaDados(query_utilizadores)

    
    def obterTodasRole(self):
        query_role = """ 
        SELECT ru.id_role, ru.nome
        FROM Role_utilizador as ru
        ORDER BY ru.id_role ASC 
        """ 
        rows = self.db.retornaListaDados(query_role)
        
        return [RoleUtilizador(
            id_role=row[0],
            nome=row[1]
        ) for row in rows]
        
    def obterCargoDepartamento(self):
        query_cargo = """ 
        SELECT f.cargo, f.departamento
        FROM Funcionario as f   
        """ 
        rows= self.db.retornaListaDados(query_cargo)
        
        return [Funcionario(
            cargo=row[0],
            departamento=row[1]
        ) for row in rows]


    def obterPassword_Username(self):
        query_password_username = """
        SELECT u.username, u.password_hash, u.id_role
        FROM utilizador  as u
        """
        return  self.db.retornaListaDados(query_password_username)
        

    def atualizarUtilizador(self, utilizador : Utilizador, funcionario : Funcionario):
        query_pessoa = """
        UPDATE Pessoa
        SET nome = %s, email=%s, telefone=%s, morada=%s, data_nascimento=%s
        WHERE id_pessoa = %s
        """
        self.db.executaQuery(query_pessoa, (utilizador.nome, utilizador.email, utilizador.telefone, utilizador.morada, utilizador.data_nascimento, utilizador.id_pessoa))
    
        query_utilizador = """
        UPDATE Utilizador
        SET username=%s, password_hash=%s, id_role=%s
        WHERE id_utilizador=%s
        """
        self.db.executaQuery(query_utilizador, (utilizador.username, utilizador.password_hash, utilizador.id_role, utilizador.id_utilizador))
        
        query_funcionario = """
        UPDATE Funcionario 
        SET cargo = %s, departamento=%s, data_contratacao=%s, salario=%s
        WHERE id_funcionario = %s
        """
        self.db.executaQuery(query_funcionario, (funcionario.cargo, funcionario.departamento, funcionario.data_contratacao, funcionario.salario, funcionario.id_funcionario))
        
    
    def eliminarUtilizador(self, id_utilizador:int):
        self.db.executaQuery("DELETE FROM Funcionario WHERE id_funcionario=%s", (id_utilizador,))
        self.db.executaQuery("DELETE FROM Utilizador WHERE id_utilizador=%s", (id_utilizador,))
        self.db.executaQuery("DELETE FROM Pessoa WHERE id_pessoa=%s", (id_utilizador,))