import tkinter as tk
from tkinter import ttk, messagebox
from Models.Cliente import Cliente
from DAL.cliente_dal import ClienteDAL
from DB.DB_Utils import PG_DB_Utils as Database

class ClienteApp:

    def __init__(self, parent, db):
        self.root = parent
        self.db = db
        self.cliente = ClienteDAL(self.db)
        # Frame do formulário
        frame_form = tk.Frame(self.root, padx=10, pady=10)
        frame_form.pack(fill="x")

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
        
        tk.Label(frame_form, text="Data de Registo:").grid(row=5, column=0, sticky="w")
        self.entry_data_registo = tk.Entry(frame_form, width=50)
        self.entry_data_registo.grid(row=5, column=1, padx=5, pady=5)
        


        # Botão para adicionar cliente
        btn_add = tk.Button(frame_form, text="Adicionar Cliente", command=self.adicionar_cliente)
        btn_add.grid(row=6, column=0, columnspan=2, pady=10)
        
        
        
        # Botão para editar cliente
        btn_add = tk.Button(frame_form, text="Editar Cliente", command=self.editar_clientes)
        btn_add.grid(row=6, column=1, columnspan=2, pady=10)
        
        
        
        #Botão para remover cliente
        btn_add = tk.Button(frame_form, text="Remover Cliente", command=self.remover_cliente)
        btn_add.grid(row=6, column=2, pady=10)
        
        
        #Botão para guardar as alterações do botão editar
        btn_add = tk.Button(frame_form, text="Guardar Alterações", command=self.guardar_edicao)
        btn_add.grid(row=2, column=5, pady=5)
        
        
        # Tabela de clientes
        self.tree = ttk.Treeview(self.root, columns=("id", "nome", "email", "telefone", "morada", "dataNascimento", "dataRegisto"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("email", text="Email")
        self.tree.heading("telefone", text="Telefone")
        self.tree.heading("morada", text="Morada")
        self.tree.heading("dataNascimento", text="DataNascimento")
        self.tree.heading("dataRegisto", text="DataRegisto")

        self.tree.column("id", width=50)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Carregar clientes existentes
        self.carregar_clientes()

    def adicionar_cliente(self):
        try:
            cliente = Cliente(
                nome=self.entry_nome.get(),
                email=self.entry_email.get(),
                telefone=self.entry_telefone.get(),
                morada=self.entry_morada.get(),
                data_nascimento=self.entry_data_nascimento.get(),
                data_registo=self.entry_data_registo.get()
            )
            cliente_id = self.cliente.criarCliente(cliente)
            messagebox.showinfo("Sucesso", f"Cliente criado com ID {cliente_id}")
            self.carregar_clientes()
            self.limpar_formulario()
        except Exception as e:
            messagebox.showerror("Erro", str(e))    


    def editar_clientes(self):
        try:
            if self.tree.focus():
                valores = self.tree.item(self.tree.focus(), "values")
                id_cliente = valores[0]
                
                self.id_cliente_editado= id_cliente

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
                
                
                self.entry_data_registo.delete(0, tk.END)
                self.entry_data_registo.insert(0, valores[6])
            else:
                messagebox.showerror("Aviso", "Selecione um cliente!")
                return
  
        except Exception as e:
            messagebox.showerror("Erro", str(e))


    def remover_cliente(self):
        cliente_selecionado = self.tree.focus()
        if not self.tree.focus():
            messagebox.showerror("Aviso", "Selecione um cliente primeiro!")
            return

        valores = self.tree.item(cliente_selecionado, "values")
        id_cliente = valores[0]

        confirm = messagebox.askyesno("Confirmar", f"Tem a certeza que deseja remover o cliente {valores[1]}?")
        if confirm:
            try:
                self.cliente.eliminarCliente(id_cliente)
                self.tree.delete(cliente_selecionado)
                messagebox.showinfo("Sucesso", "Cliente removido com sucesso!")
                self.limpar_formulario()
            except Exception as e:
                messagebox.showerror("Error", f"Não foi possível remover o cliente: {e}")


    def carregar_clientes(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        clientes = self.cliente.obterTodosClientes()
        for c in clientes:
            self.tree.insert("", "end", values=(c.id_cliente, c.nome, c.email, c.telefone, c.morada, c.data_nascimento, c.data_registo))



    def guardar_edicao(self):
        if self.id_cliente_editado is None:
            messagebox.showerror("Erro", "Nenhum cliente em edição.")
            return

        confirm = messagebox.askyesno("Aviso", "Deseja guardar as alterações?")
        if not confirm:
            return
            
        try:
            cliente = Cliente(
                id_cliente = self.id_cliente_editado,
                nome=self.entry_nome.get(),
                email=self.entry_email.get(),
                telefone=self.entry_telefone.get(),
                morada=self.entry_morada.get(),
                data_nascimento=self.entry_data_nascimento.get(),
                data_registo=self.entry_data_registo.get()
            )
            self.cliente.atualizarCliente(cliente)
            messagebox.showinfo("Sucesso", f"Cliente atualizado com sucesso!")
            self.carregar_clientes()
            self.limpar_formulario()
                
    
            self.id_cliente_editado = None
        except Exception as e: 
            messagebox.showerror("Erro", str(e))
   
    def limpar_formulario(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_telefone.delete(0, tk.END)
        self.entry_morada.delete(0, tk.END)
        self.entry_data_nascimento.delete(0, tk.END)
        self.entry_data_registo.delete(0, tk.END)
         
