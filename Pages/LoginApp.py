import tkinter as tk
from tkinter import ttk, messagebox
from Models.RoleUtilizador import RoleUtilizador
from DB.DB_Utils import PG_DB_Utils as Database



class LoginApp:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.Roleutil = RoleUtilizador(self.db)
        frame_form = tk.Frame(self.root, padx=10, pady=10)
        frame_form.pack(fill="x")
        
        tk.Label(frame_form, text="Utilizador:").grid(row=0, column=0, sticky="w")
        self.entry_util = tk.Entry(frame_form, width=40)
        self.entry_util.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Labeç(frame_form, text="Palavra-passe:").grid(row=1, column=0, sticky="w")
        self.entry_password = tk.Entry(frame_form, width=40)
        self.entry_password.grid(row=1, column=1, padx=5, pady=5)
        
        
        