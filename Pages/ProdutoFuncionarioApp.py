import tkinter as tk 
from tkinter import ttk, messagebox 
from Models.Produto import Produto
from DAL.produto_dal import ProdutoDAL
from DB.DB_Utils import PG_DB_Utils as Database
from DAL.categoria_dal import CategoriaDAL


class ProdutoFuncionarioApp:

    def __init__(self, parent, db):
        self.root = parent
        self.db = db
        self.produto_dal = ProdutoDAL(self.db)
        self.categoria_dal = CategoriaDAL(self.db)
        self.categorias = self.categoria_dal.obterTodasCategorias()

        # Tabela de clientes
        self.tree = ttk.Treeview(self.root, columns=("id", "nome","preco", "stock","categoria"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("preco", text="Preço")
        self.tree.heading("stock", text="Stock")
        self.tree.heading("categoria", text="Categoria")

        self.tree.column("id", width=50)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Carregar clientes existentes
        self.carregar_produtos()

    def carregar_produtos(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        produtos = self.produto_dal.obterTodosProdutos()
        for p in produtos:
            self.tree.insert("", "end", values=(p.id_produto, p.nome, p.preco, p.stock, p.id_categoria))


         


         
