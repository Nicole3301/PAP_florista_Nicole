from Models.Funcionario import Funcionario

class FuncionarioDAL:
    def __init__(self, db):
        self.db = db



    def criarFuncionario(self, funcionario: Funcionario):
        
        query = """
        INSERT INTO Pessoa (nome, email, telefone, morada, data_nascimento)
        VALUES (%s, %s, %s, %s, %s) RETURNING id_pessoa
        """
        pessoa_id = self.db.retornaDado(query, (funcionario.nome, funcionario.email, funcionario.telefone, funcionario.morada, funcionario.data_nascimento))[0]


        query_funcionario = """
        INSERT INTO Funcionario (id_funcionario, cargo, departamanento, salario, data_contratacao)
        VALUES (%s, %s, %s, %s, %s)
        """
        self.db.executaQuery(query_funcionario, (pessoa_id, funcionario.cargo, funcionario.departamento, funcionario.salario, funcionario.data_contratacao))
        return pessoa_id



    def obterTodosFuncionarios(self):
        query = """
        SELECT p.id_pessoa, p.nome, p.email, p.telefone, p.morada, p.data_nascimento, f.cargo, f.departamento, f.salario, f.data_contratacao
        FROM Funcionario f
        INNER JOIN Pessoa p ON f.id_funcionario = p.id_pessoa
		ORDER BY p.id_pessoa ASC;
        """
        rows = self.db.retornaListaDados(query)
        
        return [Funcionario(
            id_funcionario=row[0],
            nome=row[1],
            email=row[2],
            telefone=row[3],
            morada=row[4],
            data_nascimento=row[5],
            cargo=row[6],
            departamento=row[7],
            salario=row[8],
            data_contratacao=row[9]
        ) for row in rows]




    def atualizarFuncionario(self, funcionario: Funcionario):
        query_pessoa = """
        UPDATE Pessoa
        SET nome=%s, email=%s, telefone=%s, morada=%s
        WHERE id_pessoa=%s
        """
        self.db.executaQuery(query_pessoa, (funcionario.nome, funcionario.email, funcionario.telefone, funcionario.morada, funcionario.id_funcionario))

        query_funcionario = """
        UPDATE Funcionario
        SET cargo=%s, departamento=%s, salario=%s, data_contratacao=%s
        WHERE id_funcionario=%s
        """
        self.db.executaQuery(query_funcionario, (funcionario.cargo, funcionario.departamento, funcionario.salario, funcionario.data_contratacao ,funcionario.id_funcionario))



        
    def eliminarFuncionario(self, id_funcionario:int):
        self.db.executaQuery("DELETE FROM Funcionario WHERE id_cliente=%s", (id_funcionario,))
        self.db.executaQuery("DELETE FROM Pessoa WHERE id_pessoa=%s", (id_funcionario,))