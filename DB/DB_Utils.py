import psycopg2
from psycopg2 import sql


class PG_DB_Utils:

    dbname = 'teste'
    user = 'postgres'
    password = '2008'
    host = '127.0.0.1'
    port = 5432


    def __init__(self):
        self.connection = None
        self.cursor = None


    ''' Estabelece a conexão com a base de dados PostgreSQL'''
    def conexao(self):

        if self.connection is None:
            try:
                self.connection = psycopg2.connect(dbname=self.dbname, user=self.user, password=self.password, host=self.host, port=self.port)
                self.cursor = self.connection.cursor()

                print("Conexão Estabelecida!")

            except Exception as e:
                self.connection = None
                self.cursor = None

                raise Exception(f"Erro na conexão à base de dados: {e}")




    ''' Fecha a conexão com a base de dados PostgreSQL'''
    def fechaConexao(self):
        if self.cursor:
            self.cursor.close()
            self.cursor = None

        if self.connection:
            self.connection.close()
            self.connection = None

        print("Conexão Fechada!")



    ''' Executa uma query SQL na base de dados (INSERT, UPDATE, DELETE)'''
    def executaQuery(self, query, params=None):

        self.conexao()

        try:
            self.cursor.execute(query, params)
            self.connection.commit()

            print("Query executada com sucesso!")

            self.fechaConexao()

        except Exception as e:
            self.connection.rollback()
            raise Exception(f"Erro ao executar a query: {e}")




    """Executa SELECT e retorna todos os resultados"""
    def retornaListaDados(self, query, params=None):
    
        self.conexao()
        try:
            self.cursor.execute(query, params)
            results = self.cursor.fetchall()
            self.fechaConexao()

            return results
        except Exception as e:
            raise Exception(f"Erro ao buscar dados: {e}")


    ''' Executa SELECT e retorna um único resultado'''
    def retornaDado(self, query, params=None):

        self.conexao()

        try:
            self.cursor.execute(query, params)
            self.connection.commit()
            result = self.cursor.fetchone()
            self.fechaConexao()

            return result

        except Exception as e:
            raise Exception(f"Erro ao buscar dado: {e}")
    


    ''' Chama uma procedure na base de dados'''
    def executaProcedure(self, procedure_name, params=None):

        self.conexao()

        try:
            self.cursor.callproc(procedure_name, params)
            self.connection.commit()

            print("Procedure chamada com sucesso!")

            self.fechaConexao()

        except Exception as e:
            self.connection.rollback()
            raise Exception(f"Erro ao chamar a procedure: {e}")

