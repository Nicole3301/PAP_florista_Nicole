import tkinter as tk
from tkinter import ttk, messagebox
from Models.Encomenda import Encomenda
from DAL.encomenda_dal import EncomendaDAL
from DB.DB_Utils import PG_DB_Utils as Database

 
class EncomendaApp:

    def __init__(self, parent, db):
        self.root = parent
        self.db = db
        self.encomenda = EncomendaDAL(self.db)
        self.id_encomenda_editada = None
    
        frame_form = tk.Frame(self.root, padx=10, pady=10)
        frame_form.pack(fill="x")
        

        # Labels e Entrys
        tk.Label(frame_form, text="Cliente:").grid(row=0, column=0, sticky="w")
        self.entry_cliente = tk.Entry(frame_form, width=50)
        self.entry_cliente.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Produtos:").grid(row=1, column=0, sticky="w")
        self.entry_produtos = tk.Entry(frame_form, width=50)
        self.entry_produtos.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Quantidade:").grid(row=2, column=0, sticky="w")
        self.entry_quantidade = tk.Entry(frame_form, width=50)
        self.entry_quantidade.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Data Entrega(AAAA-MM-DD):").grid(row=3, column=0, sticky="w")
        self.entry_dataEntrega = tk.Entry(frame_form, width=50)
        self.entry_dataEntrega.grid(row=3, column=1, padx=5, pady=5)


        # Botão para adicionar cliente
        btn_add = tk.Button(frame_form, text="Adicionar Encomenda", command=self.adicionar_encomenda)
        btn_add.grid(row=6, column=0, columnspan=2, pady=10)
         
        # Botão para editar cliente
        btn_add = tk.Button(frame_form, text="Editar Encomenda", command=self.editar_encomenda)
        btn_add.grid(row=6, column=1, pady=10)
        
        #Botão para remover cliente
        btn_add = tk.Button(frame_form, text="Remover Encomenda", command=self.remover_encomenda)
        btn_add.grid(row=6, column=2, pady=10)
        
        #Botão para guardar as alterações do botão editar
        btn_add = tk.Button(frame_form, text="Guardar Alterações", command=self.guardar_edicao)
        btn_add.grid(row=2, column=5, pady=5)
        
        btn_add = tk.Button(frame_form, text="Fatura")
        btn_add.grid(row=2, column=6, pady=5)
        
        
        # Tabela de clientes
        self.tree = ttk.Treeview(self.root, columns=("id", "cliente", "produto", "quantidade", "dataEntrega"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("cliente", text="cliente")
        self.tree.heading("produto", text="Produtos")
        self.tree.heading("quantidade", text="Quantidade")
        self.tree.heading("dataEntrega", text="Data Entrega")
        self.tree.column("id", width=50)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree.bind("<Double-Button-1>", self.abrir_nova_janela)

        # Carregar clientes existentes
        self.carregar_encomendas()

    def adicionar_encomenda(self):
        try:
            encomenda = Encomenda(
                cliente=self.entry_cliente.get(),
                produtos=self.entry_produtos.get(),
                quantidade=self.entry_quantidade.get(),
                dataEntrega=self.entry_dataEntrega.get(),   
                estado = "pendente"
            )
            id_encomenda = self.encomenda.criarEncomenda(encomenda)
            messagebox.showinfo("Sucesso", f"Encomenda criada com ID {id_encomenda}")
            self.carregar_encomendas()
            self.limpar_formulario()
        except Exception as e:
            messagebox.showerror("Erro", str(e))    


    def editar_encomenda(self):
        try:
            if self.tree.focus():
                valores = self.tree.item(self.tree.focus(), "values")
                id_encomenda = valores[0]
                
                self.id_encomenda_editada= id_encomenda

                self.entry_cliente.delete(0, tk.END)
                self.entry_cliente.insert(0, valores[1])

                self.entry_produtos.delete(0, tk.END)
                self.entry_produtos.insert(0, valores[2])

                self.entry_quantidade.delete(0, tk.END)
                self.entry_quantidade.insert(0, valores[3])

                self.entry_dataEntrega.delete(0, tk.END)
                self.entry_dataEntrega.insert(0, valores[4])
            else:
                messagebox.showerror("Aviso", "Selecione uma encomenda!")
                return
  
        except Exception as e:
            messagebox.showerror("Erro", str(e))


    def remover_encomenda(self):
        encomenda_selecionada = self.tree.focus()
        if not self.tree.focus():
            messagebox.showerror("Aviso", "Selecione uma encomenda primeiro!")
            return

        valores = self.tree.item(encomenda_selecionada, "values")
        id_encomenda = valores[0]

        confirm = messagebox.askyesno("Confirmar", f"Tem a certeza que deseja remover a encomenda {valores[1]}?")
        if confirm:
            try:
                self.encomenda.eliminarEncomenda(id_encomenda)
                self.tree.delete(encomenda_selecionada)
                messagebox.showinfo("Sucesso", "Encomenda removida com sucesso!")
                self.limpar_formulario()
            except Exception as e:
                messagebox.showerror("Error", f"Não foi possível remover a encomenda: {e}")


    def carregar_encomendas(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        encomendas = self.encomenda.obterTodasEncomendas()
        for e in encomendas:
            self.tree.insert("", "end", values=(e.id_encomenda, e.id_cliente, e.data_encomenda, ))



    def guardar_edicao(self):
        if self.id_encomenda_editada is None:
            messagebox.showerror("Erro", "Nenhuma encomenda em edição.")
            return

        confirm = messagebox.askyesno("Aviso", "Deseja guardar as alterações?")
        if not confirm:
            return
            
        try:
            encomenda = Encomenda(
                id_encomemda = self.id_encomenda_editada,
                cliente=self.entry_cliente.get(),
                produtos=self.entry_produtos.get(),
                quantidade=self.entry_quantidade.get(),
                dataEntrega=self.entry_dataEntrega.get()
            )
            self.encomenda.atualizarEncomenda(encomenda)
            messagebox.showinfo("Sucesso", f"Encomenda atualizada com sucesso!")
            self.carregar_encomendas()
            self.limpar_formulario()
                
    
            self.id_encomenda_editada = None
        except Exception as e: 
            messagebox.showerror("Erro", str(e))
   
    def limpar_formulario(self):
        self.entry_cliente.delete(0, tk.END)
        self.entry_produtos.delete(0, tk.END)
        self.entry_quantidade.delete(0, tk.END)
        self.entry_dataEntrega.delete(0, tk.END)
    
    
    def abrir_nova_janela(self):
        janala_secundaria = tk.Toplevel(self.tree)
        janala_secundaria.title("Informações da Encomenda")
        
        tk.Button(janala_secundaria, text="Fechar", command=janala_secundaria.destroy).pack()
