import tkinter as tk
from tkinter import ttk, messagebox
from Models.Cliente import Cliente
from DAL.cliente_dal import ClienteDAL
from DB.DB_Utils import PG_DB_Utils as Database
from Pages.ClienteApp import ClienteApp 
from Pages.ProdutoApp import ProdutoApp 
from Pages.CategoriaApp import CategoriaApp
from Pages.EncomendaApp import EncomendaApp
from Pages.PromocaoApp import PromocaoApp
from Pages.FaturaApp import FaturaApp

   
class Interface():    
    def __init__(self, root):
        self.root = root
        self.root.title("BloomStore")
        #self.root.geometry("800x500")
        # mudar o icon da janela
        self.root.iconbitmap(r'C:\Users\Utilizador\Downloads\PAP_florista_Nicole Almeida\PAP_florista_Nicole\Imagem\icon-flor.ico')
        
        #tamanho da janela
        largura = 800 
        altura = 500
        
        #calculos para ficar centralizado no meio do ecra do computador
        largura_screen = root.winfo_screenwidth()
        altura_screen = root.winfo_screenheight()

        print(altura_screen, largura_screen)
        
        posx = largura_screen/2 - largura/2
        posy= altura_screen/2 - altura/2
        
        root.geometry("%dx%d+%d+%d" % (largura, altura, posx, posy))

        # Inicializar BD e DAL
        self.db = Database()
        
        notebook = ttk.Notebook(root)
        notebook.pack(expand=True, fill='both') 
    
        frame_cliente = ttk.Frame(notebook, width=800, height=500)
        frame_produto = ttk.Frame(notebook, width=800, height=500)
        frame_categoria = ttk.Frame(notebook, width=800, height=500)
        frame_encomenda = ttk.Frame(notebook, width=800, height=500)
        frame_funcionario = ttk.Frame(notebook, width=800, height=500)
        frame_promocao = ttk.Frame(notebook, width=800, height=500)
        frame_fatura = ttk.Frame(notebook, width=800, height=500)
    
        frame_cliente.pack(fill='both', expand=True)
        frame_produto.pack(fill='both', expand=True)
        frame_categoria.pack(fill='both', expand=True)
        frame_encomenda.pack(fill='both', expand=True)
        frame_funcionario.pack(fill='both', expand=True)
        frame_promocao.pack(fill='both', expand=True)
        frame_fatura.pack(fill='both', expand=True)

        # add frames to notebook

        notebook.add(frame_cliente, text='Cliente')
        notebook.add(frame_produto, text='Produto')
        notebook.add(frame_categoria, text="Categoria")
        notebook.add(frame_encomenda, text='Encomenda')
        notebook.add(frame_funcionario, text='Funcionário')
        notebook.add(frame_promocao, text="Promoção")
        notebook.add(frame_fatura, text="Fatura")
        
        ClienteApp(frame_cliente, self.db)
        ProdutoApp(frame_produto, self.db)
        CategoriaApp(frame_categoria, self.db)
        EncomendaApp(frame_encomenda, self.db)
        PromocaoApp(frame_promocao, self.db)
        FaturaApp(frame_fatura, self.db)
        
     
    
if __name__ == "__main__":
    root = tk.Tk()
    app = Interface(root)
    root.mainloop()
