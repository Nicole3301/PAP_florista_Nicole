import tkinter as tk
from tkinter import ttk, messagebox
from Models.Categoria import CategoriaProduto
from DAL.categoria_dal import CategoriaDAL
from DB.DB_Utils import PG_DB_Utils as Database

class CategoriaFuncionarioApp:

    def __init__(self, parent, db):
        self.root = parent
        self.db = db
        self.categoria = CategoriaDAL(self.db)
        
        # Tabela de clientes
        self.tree = ttk.Treeview(self.root, columns=("id", "nome", "descricao"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("descricao", text="Descrição")
        self.tree.column("id", width=50)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Carregar clientes existentes
        self.carregar_categoria() 

    def carregar_categoria(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        categorias = self.categoria.obterTodasCategorias()
        for c in categorias:
            self.tree.insert("", "end", values=(c.id_categoria, c.nome, c.descricao))




         
