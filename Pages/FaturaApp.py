import tkinter as tk
from tkinter import ttk, messagebox
from Models.Fatura import Fatura
from DAL.fatura_dal import FaturaDAL
from DB.DB_Utils import PG_DB_Utils as Database

class FaturaApp:

    def __init__(self, parent, db):
        self.root = parent
        self.db = db
        self.fatura = FaturaDAL(self.db)
        # Frame do formulário
        frame_form = tk.Frame(self.root, padx=10, pady=10)
        frame_form.pack(fill="x")


        # Botão para adicionar cliente
        btn_adicionar = tk.Button(frame_form, text="Adicionar promocao", command=self.imprimir_fatura, bg="white", height=1)
        btn_adicionar.grid(row=4, column=0, pady=10)
        #btn_adicionar.config(activebackground="pink", activeforeground="white")
        
        
        self.tree = ttk.Treeview(self.root, columns=("id", "nome", "desconto", "data_inicio", "data_fim"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("desconto", text="Desconto")
        self.tree.heading("data_inicio", text="Data Inicio")
        self.tree.heading("data_fim", text="Data Fim")
        
        self.tree.column("id", width=50)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.carregar_fatura()

    def imprimir_fatura(self, event):
        pass


    def carregar_fatura(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        fatura = self.fatura.obterTodasFaturas()
        for f in fatura:
            self.tree.insert("", "end", values=())


