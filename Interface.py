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
from Pages.UtilizadorApp import UtilizadorApp
from DAL.utilizador_dal import UtilizadorDAL
from Pages.ProdutoFuncionarioApp import ProdutoFuncionarioApp
from Pages.CategoriaFuncionarioApp import CategoriaFuncionarioApp
from Pages.PromocaoFuncionarioApp import PromocaoFuncionarioApp
import bcrypt 
from Pages.UtilizadorApp import UtilizadorApp


class Interface():    
    def __init__(self, root):
        self.root = root
        self.root.title("BloomStore")
        # Inicializar BD e DAL
        self.db = Database()
        #self.root.geometry("800x500")
        # mudar o icon da janela
        self.root.iconbitmap(r'C:\Users\Utilizador\Downloads\PAP_florista_Nicole Almeida\PAP_florista_Nicole\Imagem\icon-flor.ico')
        frame_form = tk.Frame(self.root, padx=10, pady=10)
        frame_form.pack(fill="x")
        self.utilizador = UtilizadorDAL(self.db)
        self.verificar_dados = self.utilizador.obterPassword_Username()
        self.id_role = self.utilizador.obterTodasRole()

        #tamanho da janela
        largura = 500
        altura = 300
        
        #calculos para ficar centralizado no meio do ecra do computador
        largura_screen = root.winfo_screenwidth()
        altura_screen = root.winfo_screenheight()

        print(altura_screen, largura_screen)
        
        posx = largura_screen/2 - largura/2
        posy= altura_screen/2 - altura/2
        
        
        root.geometry("%dx%d+%d+%d" % (largura, altura, posx, posy))

         
        tk.Label(frame_form, text="Login").grid(row=0, column=7, sticky="nsew")        
        
        tk.Label(frame_form, text="Username:").grid(row=1, column=6, sticky="nsew")
        self.entry_username = tk.Entry(frame_form, width=25)
        self.entry_username.grid(row=1, column=7, padx=12, pady=1)
        #self.entry_username.grid(row=1, column=3, padx=(largura/2)-20, pady=1)

        tk.Label(frame_form, text="Password:").grid(row=2, column=6, sticky="nsew")
        self.entry_password = tk.Entry(frame_form, width=25, show="*")
        self.entry_password.grid(row=2, column=7, padx=12, pady=5)

        btn_login = tk.Button(frame_form, text="Login", command=self.verificar_login, width=17, bg="white", height=1)
        btn_login.grid(row=3, column=7, pady=20, padx=5)
      

    def abrir_janela(self):
        self.password_username = UtilizadorDAL(self.db)
        self.root.iconbitmap(r'C:\Users\Utilizador\Downloads\PAP_florista_Nicole Almeida\PAP_florista_Nicole\Imagem\icon-flor.ico')
        janela_admin = tk.Toplevel(self.root)
        notebook = ttk.Notebook(janela_admin)
        notebook.pack(expand=True, fill='both') 
        #tamanho da janela
        largura = 800 
        altura = 500
        
        #calculos para ficar centralizado no meio do ecra do computador
        largura_screen = root.winfo_screenwidth()
        altura_screen = root.winfo_screenheight()

        print(altura_screen, largura_screen)
        
        posx = largura_screen/2 - largura/2
        posy= altura_screen/2 - altura/2
        
        janela_admin.geometry("%dx%d+%d+%d" % (largura, altura, posx, posy))
        
        frame_cliente = ttk.Frame(notebook, width=800, height=500)
        frame_produto = ttk.Frame(notebook, width=800, height=500)
        frame_categoria = ttk.Frame(notebook, width=800, height=500)
        frame_encomenda = ttk.Frame(notebook, width=800, height=500)
        frame_promocao = ttk.Frame(notebook, width=800, height=500)
        frame_utilizador = ttk.Frame(notebook, width=800, height=500)
                
        frame_cliente.pack(fill='both', expand=True)
        frame_produto.pack(fill='both', expand=True)
        frame_categoria.pack(fill='both', expand=True)
        frame_encomenda.pack(fill='both', expand=True)
        frame_promocao.pack(fill='both', expand=True)
        frame_utilizador.pack(fill='both', expand=True)

        notebook.add(frame_cliente, text='Cliente')
        notebook.add(frame_produto, text='Produto')
        notebook.add(frame_categoria, text="Categoria")
        notebook.add(frame_encomenda, text='Encomenda')
        notebook.add(frame_promocao, text="Promoção")
        notebook.add(frame_utilizador, text="Utilizadores")
        
        ClienteApp(frame_cliente, self.db)
        ProdutoApp(frame_produto, self.db)
        CategoriaApp(frame_categoria, self.db)
        EncomendaApp(frame_encomenda, self.db)
        PromocaoApp(frame_promocao, self.db)
        UtilizadorApp(frame_utilizador, self.db)
        
        
    def abrir_janela_funcionario(self):
        self.password_username = UtilizadorDAL(self.db)
        janela_funcionario = tk.Toplevel(self.root)
        self.root.iconbitmap(r'C:\Users\Utilizador\Downloads\PAP_florista_Nicole Almeida\PAP_florista_Nicole\Imagem\icon-flor.ico')
        notebook = ttk.Notebook(janela_funcionario)
        notebook.pack(expand=True, fill='both') 
        #tamanho da janela
        largura = 800 
        altura = 500
        
        #calculos para ficar centralizado no meio do ecra do computador
        largura_screen = root.winfo_screenwidth()
        altura_screen = root.winfo_screenheight()

        print(altura_screen, largura_screen)
        
        posx = largura_screen/2 - largura/2
        posy= altura_screen/2 - altura/2
        
        janela_funcionario.geometry("%dx%d+%d+%d" % (largura, altura, posx, posy))
    
        frame_cliente = ttk.Frame(notebook, width=800, height=500)
        frame_produto = ttk.Frame(notebook, width=800, height=500)
        frame_categoria = ttk.Frame(notebook, width=800, height=500)
        frame_encomenda = ttk.Frame(notebook, width=800, height=500)
        frame_promocao = ttk.Frame(notebook, width=800, height=500)
                
        frame_cliente.pack(fill='both', expand=True)
        frame_produto.pack(fill='both', expand=True)
        frame_categoria.pack(fill='both', expand=True)
        frame_encomenda.pack(fill='both', expand=True)
        frame_promocao.pack(fill='both', expand=True)

        notebook.add(frame_cliente, text='Cliente')
        notebook.add(frame_produto, text='Produto')
        notebook.add(frame_categoria, text="Categoria")
        notebook.add(frame_encomenda, text='Encomenda')
        notebook.add(frame_promocao, text="Promoção")
        
        ClienteApp(frame_cliente, self.db)
        ProdutoFuncionarioApp(frame_produto, self.db)
        CategoriaFuncionarioApp(frame_categoria, self.db)
        PromocaoFuncionarioApp(frame_promocao, self.db)
        EncomendaApp(frame_encomenda, self.db)
    
    
        
    def verificar_login(self):
        username_inserido = self.entry_username.get()
        password_inserido = self.entry_password.get()
             
        print(self.verificar_dados) 
    
        # normal
        """ 
        for utilizador in self.verificar_dados:
            role = utilizador[2]
            if username_inserido==utilizador[0] and password_inserido==utilizador[1]:
                if role == 1:            
                        messagebox.showinfo("sucesso", "O login foi bem sucedido!")
                        root.withdraw() # esconde a janela
                        self.abrir_janela()
                        return
                elif role == 2:
                        messagebox.showinfo("sucesso", "O login foi bem sucedido!")
                        root.withdraw() # esconde a janela
                        self.abrir_janela_funcionario()
                        return
            else:
                messagebox.showinfo("Erro", "O username ou a password estão errados.")  
                
        self.entry_username.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)    
        """ 
    
        #incriptado
        for utilizador in self.verificar_dados:
            username, password_hash, role = utilizador
            if username_inserido == username:
                if bcrypt.checkpw(password_inserido.encode('utf-8'), password_hash.encode('utf-8')):
                    messagebox.showinfo("Sucesso", "O login foi bem sucedido!")
                    root.withdraw()
                    if role == 1:            
                        #messagebox.showinfo("sucesso", "O login foi bem sucedido!")
                        #root.withdraw() # esconde a janela
                        self.abrir_janela()
                        return
                    elif role == 2:
                        #messagebox.showinfo("sucesso", "O login foi bem sucedido!")
                        #root.withdraw() # esconde a janela
                        self.abrir_janela_funcionario()
                        return
                else:
                    messagebox.showerror("Erro","Password incorreta.")
                    self.entry_password.delete(0, tk.END)
                    return
                    
        messagebox.showinfo("Erro", "O username ou a password estão errados.")  
                      
        self.entry_username.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)
       
        

if __name__ == "__main__":
    root = tk.Tk()
    app = Interface(root)
    root.mainloop()
    
