import tkinter as tk
from tkinter import ttk, messagebox
from Models.Utilizador import Utilizador
from DAL.utilizador_dal import UtilizadorDAL
from DB.DB_Utils import PG_DB_Utils as Database
from DAL.funcionario_dal import FuncionarioDAL
from Models.Funcionario import Funcionario
from hashlib import sha256
import datetime 

class UtilizadorApp:

    def __init__(self, parent, db):
        self.root = parent
        self.db = db
        self.utilizador_dal = UtilizadorDAL(self.db)
        self.role_utilizador = self.utilizador_dal.obterTodasRole()
        self.funcionario_dal = FuncionarioDAL(self.db)
        self.funcionario = self.funcionario_dal.obterTodosFuncionarios()
        # Frame do formulário
        frame_form = tk.Frame(self.root, padx=10, pady=10)
        frame_form.pack(fill="x")
        style = ttk.Style()

        # Labels e Entrys
        tk.Label(frame_form, text="Nome:").grid(row=0, column=0, sticky="w")
        self.entry_nome = tk.Entry(frame_form, width=50)
        self.entry_nome.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Email:").grid(row=1, column=0, sticky="w")
        self.entry_email = tk.Entry(frame_form, width=50)
        self.entry_email.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Telefone:").grid(row=2, column=0, sticky="w")
        self.entry_telefone = tk.Entry(frame_form, width=50)
        self.entry_telefone.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Morada:").grid(row=3, column=0, sticky="w")
        self.entry_morada = tk.Entry(frame_form, width=50)
        self.entry_morada.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Data de Nascimento (YYYY-MM-DD):").grid(row=4, column=0, sticky="w")
        self.entry_data_nascimento = tk.Entry(frame_form, width=50)
        self.entry_data_nascimento.grid(row=4, column=1, padx=5, pady=5)
        
        tk.Label(frame_form, text="Username:").grid(row=5, column=0, sticky="w")
        self.entry_username= tk.Entry(frame_form, width=50)
        self.entry_username.grid(row=5, column=1, padx=5, pady=5)
        
        tk.Label(frame_form, text="Password:").grid(row=6, column=0, sticky="w")
        self.entry_password = tk.Entry(frame_form, width=50)
        self.entry_password.grid(row=6, column=1, padx=5, pady=5)

        
     
        tk.Label(frame_form, text="Função:").grid(row=7, column=0, sticky="w")
        self.entry_id_funcao = ttk.Combobox(frame_form, width=47)
        self.entry_id_funcao.grid(row=7, column=1, padx=5, pady=5)
        
        self.entry_id_funcao['values'] = [ru.nome for ru in self.role_utilizador]
        
        tk.Label(frame_form, text="Cargo:").grid(row=1, column=3, sticky="w")
        self.entry_cargo = ttk.Combobox(frame_form, width=47)
        self.entry_cargo.grid(row=1, column=4, padx=5, pady=5)
        
        self.entry_cargo['values'] = [f.cargo for f in self.funcionario]  
        
        tk.Label(frame_form, text="Departamento:").grid(row=2, column=3, sticky="w")
        self.entry_departamento = ttk.Combobox(frame_form, width=47)
        self.entry_departamento.grid(row=2, column=4, padx=5, pady=5)
        
        self.entry_departamento['values'] = [f.departamento for f in self.funcionario]
        
        tk.Label(frame_form, text="Salário:").grid(row=3, column=3, sticky="w")
        self.entry_salario= tk.Entry(frame_form, width=47)
        self.entry_salario.grid(row=3, column=4, padx=5, pady=5)
        
        tk.Label(frame_form, text="Data Contratação:").grid(row=4, column=3, sticky="w")
        self.entry_data_contratacao = tk.Entry(frame_form, width=47)
        self.entry_data_contratacao.grid(row=4, column=4, padx=5, pady=5)


        btn_adicionar = tk.Button(frame_form, text="Adicionar Utilizador", command=self.adicionar_utilizador,bg="white")
        btn_adicionar.grid(row=9, column=0, columnspan=2, pady=10)
        #btn_adicionar.config(activebackground="pink", activeforeground="white")
        
        btn_editar = tk.Button(frame_form, text="Editar Utilizador", command=self.editar_utilizador,bg="white")
        btn_editar.grid(row=9, column=1, columnspan=2, pady=10)
        
        btn_remover = tk.Button(frame_form, text="Remover Utilizador", command=self.remover_utilizador,bg="white")
        btn_remover.grid(row=9, column=2, pady=10)
        
        btn_guardar = tk.Button(frame_form, text="Guardar Alterações", command=self.guardar_edicao,bg="white")
        btn_guardar.grid(row=5, column=5, pady=5)
        
        
        # Tabela de clientes
        self.tree = ttk.Treeview(self.root, columns=("id", "nome", "email", "telefone", "morada", "dataNascimento", "username", "password", "role"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("email", text="Email")
        self.tree.heading("telefone", text="Telefone")
        self.tree.heading("morada", text="Morada")
        self.tree.heading("dataNascimento", text="DataNascimento")
        self.tree.heading("username", text="Username")
        self.tree.heading("password", text="Password")
        self.tree.heading("role", text="Função")
        
        self.tree.column("id", width=50)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.carregar_utilizadores()

    def adicionar_utilizador(self):
        try:
            """ 
            hash = sha256(password.encode())
            self.passwordHash = hash.hexdigest()
            """
            password = self.entry_password.get()
            

            id_role = self.get_id_role(self.entry_id_funcao.get())
            if not id_role:
                messagebox.showerror("Erro", "Função inválida.")
                return
                
            cargo = self.get_id_cargo(self.entry_cargo.get())
            if not cargo:
                messagebox.showerror("Erro", "Cargo inválido.")
                return
                
            departamento = self.get_id_departamento(self.entry_departamento.get())
            if not departamento:
                messagebox.showerror("Erro", "Departamento inválido.") 
                return                               
                
            utilizador = Utilizador(
                nome=self.entry_nome.get(),
                email=self.entry_email.get(),
                telefone=self.entry_telefone.get(),
                morada=self.entry_morada.get(),
                data_nascimento=self.entry_data_nascimento.get(),
                username=self.entry_username.get(),
                password_hash=password,
                id_role=id_role
            )
            funcionario = Funcionario(
                cargo=cargo,
                departamento=departamento,
                salario=self.entry_salario.get(),
                data_contratacao=self.entry_data_contratacao.get()                                              
            )
            id_utilizador = self.utilizador_dal.criarUtilizador(utilizador, funcionario)
            messagebox.showinfo("Sucesso", f"Utilizador criado com ID {id_utilizador}")
            password_hash = sha256(password.encode()).hexdigest()
            self.carregar_utilizadores()
            self.limpar_formulario()
        except Exception as e:
            messagebox.showerror("Erro", str(e))    


    def editar_utilizador(self):
        try:
            if self.tree.focus():
                valores = self.tree.item(self.tree.focus(), "values")
                id_utilizador = valores[0]
                
                self.id_utilizador_editado= id_utilizador

                self.entry_nome.delete(0, tk.END)
                self.entry_nome.insert(0, valores[1])

                self.entry_email.delete(0, tk.END)
                self.entry_email.insert(0, valores[2])

                self.entry_telefone.delete(0, tk.END)
                self.entry_telefone.insert(0, valores[3])

                self.entry_morada.delete(0, tk.END)
                self.entry_morada.insert(0, valores[4])
                
                self.entry_data_nascimento.delete(0, tk.END)
                self.entry_data_nascimento.insert(0, valores[5])
                
                self.entry_username.delete(0, tk.END)
                self.entry_username.insert(0, valores[6])
                
                self.entry_password.delete(0, tk.END)
                self.entry_password.insert(0, valores[7])
                
                self.entry_id_funcao.delete(0, tk.END)
                self.entry_id_funcao.insert(0, valores[8])
            else:
                messagebox.showerror("Aviso", "Selecione um utilizador!")
                return
  
        except Exception as e:
            messagebox.showerror("Erro", str(e))


    def remover_utilizador(self):
        utilizador_selecionado = self.tree.focus()
        if not self.tree.focus():
            messagebox.showerror("Aviso", "Selecione um utilizador primeiro!")
            return

        valores = self.tree.item(utilizador_selecionado, "values")
        id_utilizador = valores[0]

        confirm = messagebox.askyesno("Confirmar", f"Tem a certeza que deseja remover o utilizador {valores[1]}?")
        if confirm:
            try:
                self.utilizador_dal.eliminarUtilizador(id_utilizador)
                self.tree.delete(utilizador_selecionado)
                messagebox.showinfo("Sucesso", "Utilizador removido com sucesso!")
                self.limpar_formulario()
            except Exception as e:
                messagebox.showerror("Error", f"Não foi possível remover o utilizador: {e}")


    def carregar_utilizadores(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        utilizadores = self.utilizador_dal.obterTodosUtilizadores()
        for u in utilizadores:
            self.tree.insert("", "end", values=(u.id_utilizador, u.username, u.password_hash, u.ultimo_login, u.id_role))


    def guardar_edicao(self):
        if self.id_utilizador_editado is None:
            messagebox.showerror("Erro", "Nenhum Utilizador em edição.")
            return

        confirm = messagebox.askyesno("Aviso", "Deseja guardar as alterações?")
        if not confirm:
            return
            
        try:
            utilizador = Utilizador(
                id_utilizador = self.id_utilizador_editado,
                username=self.entry_username.get(),
                password_hash=self.entry_password.get(),
                id_role=self.entry_id_funcao.get(),
            )
            self.utilizador_dal.atualizarUtilizador(utilizador)
            messagebox.showinfo("Sucesso", f"Utilizador atualizado com sucesso!")
            self.carregar_utilizadores()
            self.limpar_formulario()
                
    
            self.id_utilizador_editado = None
        except Exception as e: 
            messagebox.showerror("Erro", str(e))
   
    def limpar_formulario(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_telefone.delete(0, tk.END)
        self.entry_morada.delete(0, tk.END)
        self.entry_data_nascimento.delete(0, tk.END)
        self.entry_username.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)
        self.entry_id_funcao.delete(0, tk.END)
        
        
    def get_id_role(self, role):
        roles = self.utilizador_dal.obterTodasRole()
        for r in roles:
            if r.nome == role:
                return r.id_role
        return None
    
    def get_id_cargo(self, cargo):
        funcionario = self.utilizador_dal.obterTodosFuncionario()
        for f in funcionario:
            if f.cargo == cargo:
                return f
        return None
    
    def get_id_departamento(self, departamento):
        funcionario = self.utilizador_dal.obterTodosFuncionario()
        for f in funcionario:
            if f.departamento == departamento:
                return f
        return None
        
    def ObterInformacoesUtilizador(self):
        utilizador_selecionado = self.tree.selection()
        if not utilizador_selecionado:
            messagebox.showerror("Erro", "Para executar este comando tem de selecionar primeiro um utilizador.")
            return
        
        item = utilizador_selecionado[0]
        valores = self.tree.item(item, "values")
        self.id_utilizador_editado = valores[0]
        
        self.janela_fatura = tk.Toplevel(self.root)
        self.janela_fatura.title(f"Informações do Utilizador")
        self.janela_fatura.geometry("700x400")


        self.tree_fatura = ttk.Treeview(self.janela_fatura, columns=("id", "cargo", "departamento", "salario", "data_contratacao"), show="headings")
        self.tree_fatura.heading("id", text="ID")
        self.tree_fatura.heading("cargo", text="Cargo")
        self.tree_fatura.heading("departamento", text="Departamento")
        self.tree_fatura.heading("salario", text="Salário")
        self.tree_fatura.heading("data_contratacao", text="Data Contratação")
        self.tree_fatura.column("id", width=50)
        self.tree_fatura.pack(fill="both", expand=True, padx=10, pady=10)

        
        
        
