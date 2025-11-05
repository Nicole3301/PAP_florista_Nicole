import tkinter as tk
from tkinter import ttk, messagebox
from Models.Promocao import Promocao
from DAL.promocao_dal import PromocaoDAL
from DB.DB_Utils import PG_DB_Utils as Database

class PromocaoFuncionarioApp:

    def __init__(self, parent, db):
        self.root = parent
        self.db = db
        self.promocao = PromocaoDAL(self.db)

        # Tabela de clientes
        self.tree = ttk.Treeview(self.root, columns=("id", "nome", "desconto", "data_inicio", "data_fim"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("desconto", text="Desconto")
        self.tree.heading("data_inicio", text="Data Inicio")
        self.tree.heading("data_fim", text="Data Fim")
        
        self.tree.column("id", width=50)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Carregar clientes existentes
        self.carregar_promocoes()

    def carregar_promocoes(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        promocoes = self.promocao.obterTodasPromocoes()
        for p in promocoes:
            self.tree.insert("", "end", values=(p.id_promocao, p.nome, p.desconto, p.data_inicio, p.data_fim))




         
