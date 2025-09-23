from DB.DB_Utils import PG_DB_Utils
from DAL.cliente_dal import ClienteDAL
from Models.Cliente import Cliente


db = PG_DB_Utils()




if __name__ == "__main__":
    
    # CRIAR CLIENTE
    '''cli = ClienteDAL(db)
    pessoaId = cli.criarCliente(
        Cliente(
            nome="André Meira",
            email="andre.meira@email.com",
            telefone="987654321",
            morada="Rua C, 555",
            data_nascimento="1983-05-15",
            data_registo="2013-11-02",
            limite_credito=20000.0
        )
    )

    print(f"Cliente criado com ID: {pessoaId}")'''


    # OBTER TODOS CLIENTES
    '''cli = ClienteDAL(db)
    Lista_clientes = cli.obterTodosClientes()
    for c in Lista_clientes:
        print(c)'''
    
    # ATUALIZAR CLIENTE
    cli = ClienteDAL(db)
    cli.atualizarCliente(
        Cliente(
            id_cliente=9,
            nome="André Silva Meira",
            email="andre.meira@email.com",
            telefone="987654321",
            morada="Rua C, 555",
            data_nascimento="1983-05-15",
            data_registo="2013-11-02",
            limite_credito=25000.0
        )   
    )