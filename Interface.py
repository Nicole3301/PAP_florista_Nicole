import tkinter as tk
from tkinter import ttk, messagebox
from Models.Cliente import Cliente
from DAL.cliente_dal import ClienteDAL
from DB.DB_Utils import PG_DB_Utils as Database
from Pages.ClienteApp import ClienteApp 
from Pages.ProdutoApp import ProdutoApp 
from Pages.CategoriaApp import CategoriaApp
from Pages.EncomendaApp import EncomendaApp
   
class Interface():    
    def __init__(self, root):
        self.root = root
        self.root.title("BloomStore")
        self.root.geometry("800x500")
        # mudar o icon da janela
        self.root.iconbitmap(r'C:\Users\Utilizador\Downloads\PAP_florista_Nicole Almeida\PAP_florista_Nicole\Imagem\icon-flor.ico')
        
        # Inicializar BD e DAO
        self.db = Database()
        self.cliente = ClienteDAL(self.db)
        self.id_cliente_editado = None
        
        notebook = ttk.Notebook(root)
        notebook.pack(expand=True, fill='both') 
    
        frame_cliente = ttk.Frame(notebook, width=800, height=500)
        frame_produto = ttk.Frame(notebook, width=800, height=500)
        frame_categoria = ttk.Frame(notebook, width=800, height=500)
        frame_encomenda = ttk.Frame(notebook, width=800, height=500)
        frame4 = ttk.Frame(notebook, width=800, height=500)
    
        frame_cliente.pack(fill='both', expand=True)
        frame_produto.pack(fill='both', expand=True)
        frame_categoria.pack(fill='both', expand=True)
        frame_encomenda.pack(fill='both', expand=True)
        frame4.pack(fill='both', expand=True)

        # add frames to notebook

        notebook.add(frame_cliente, text='Cliente')
        notebook.add(frame_produto, text='Produto')
        notebook.add(frame_categoria, text="Categoria")
        notebook.add(frame_encomenda, text='Encomenda')
        notebook.add(frame4, text='Funcionario')
        
        ClienteApp(frame_cliente, self.db)
        ProdutoApp(frame_produto, self.db)
        CategoriaApp(frame_categoria, self.db)
        EncomendaApp(frame_encomenda, self.db)
     
    
if __name__ == "__main__":
    root = tk.Tk()
    app = Interface(root)
    root.mainloop()
