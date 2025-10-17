import tkinter as tk
from tkinter import ttk, messagebox
from Models.Promocao import Promocao
from DAL.promocao_dal import PromocaoDAL
from DB.DB_Utils import PG_DB_Utils as Database

class PromocaoApp:

    def __init__(self, parent, db):
        self.root = parent
        self.db = db
        self.promocao = PromocaoDAL(self.db)
        # Frame do formulário
        frame_form = tk.Frame(self.root, padx=10, pady=10)
        frame_form.pack(fill="x")

        # Labels e Entrys
        tk.Label(frame_form, text="Nome:").grid(row=0, column=0, sticky="w")
        self.entry_nome = tk.Entry(frame_form, width=50)
        self.entry_nome.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Desconto:").grid(row=1, column=0, sticky="w")
        self.entry_desconto = tk.Entry(frame_form, width=50)
        self.entry_desconto.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Data Inicio:").grid(row=2, column=0, sticky="w")
        self.entry_data_inicio = tk.Entry(frame_form, width=50)
        self.entry_data_inicio.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Data Fim:").grid(row=3, column=0, sticky="w")
        self.entry_data_fim = tk.Entry(frame_form, width=50)
        self.entry_data_fim.grid(row=3, column=1, padx=5, pady=5)


        # Botão para adicionar cliente
        btn_adicionar = tk.Button(frame_form, text="Adicionar promocao", command=self.adicionar_promocao)
        btn_adicionar.grid(row=4, column=0, pady=10)
        #btn_adicionar.config(activebackground="pink", activeforeground="white")
        
        # Botão para editar cliente
        btn_editar = tk.Button(frame_form, text="Editar promocao", command=self.editar_promocao)
        btn_editar.grid(row=4, column=1, pady=10)
        
        #Botão para remover cliente
        btn_remover = tk.Button(frame_form, text="Remover promocao", command=self.remover_promocao)
        btn_remover.grid(row=4, column=2, pady=10)
        
        #Botão para guardar as alterações do botão editar
        btn_guardar = tk.Button(frame_form, text="Guardar Alterações", command=self.guardar_edicao)
        btn_guardar.grid(row=2, column=5, pady=5)
        
        
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

    def adicionar_promocao(self):
        try:
            promocao = Promocao(
                nome=self.entry_nome.get(),
                desconto=self.entry_desconto.get(),
                data_inicio=self.entry_data_inicio.get(),
                data_fim=self.entry_data_fim.get()
            )
            id_promocao = self.promocao.criarPromocao(promocao)
            messagebox.showinfo("Sucesso", f"Promoção criada com ID {id_promocao}")
            self.carregar_promocoes()
            self.limpar_formulario()
        except Exception as e:
            messagebox.showerror("Erro", str(e))    


    def editar_promocao(self):
        try:
            if self.tree.focus():
                valores = self.tree.item(self.tree.focus(), "values")
                id_promocao = valores[0]
                
                self.id_promocao_editada= id_promocao

                self.entry_nome.delete(0, tk.END)
                self.entry_nome.insert(0, valores[1])

                self.entry_desconto.delete(0, tk.END)
                self.entry_desconto.insert(0, valores[2])

                self.entry_data_inicio.delete(0, tk.END)
                self.entry_data_inicio.insert(0, valores[3])

                self.entry_data_fim.delete(0, tk.END)
                self.entry_data_fim.insert(0, valores[4])
                
            else:
                messagebox.showerror("Aviso", "Selecione uma promoção!")
                return
  
        except Exception as e:
            messagebox.showerror("Erro", str(e))


    def remover_promocao(self):
        promocao_selecionada = self.tree.focus()
        if not self.tree.focus():
            messagebox.showerror("Aviso", "Selecione uma promoção primeiro!")
            return

        valores = self.tree.item(promocao_selecionada, "values")
        id_promocao = valores[0]

        confirm = messagebox.askyesno("Confirmar", f"Tem a certeza que deseja remover a promoção {valores[1]}?")
        if confirm:
            try:
                self.promocao.eliminarPromocao(id_promocao)
                self.tree.delete(promocao_selecionada)
                messagebox.showinfo("Sucesso", "Promoção removida com sucesso!")
                self.limpar_formulario()
            except Exception as e:
                messagebox.showerror("Error", f"Não foi possível remover a promoção: {e}")


    def carregar_promocoes(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        promocoes = self.promocao.obterTodasPromocoes()
        for p in promocoes:
            self.tree.insert("", "end", values=(p.id_promocao, p.nome, p.desconto, p.data_inicio, p.data_fim))



    def guardar_edicao(self):
        if self.id_promocao_editada is None:
            messagebox.showerror("Erro", "Nenhuma promoção em edição.")
            return

        confirm = messagebox.askyesno("Aviso", "Deseja guardar as alterações?")
        if not confirm:
            return
            
        try:
            promocao= Promocao(
                id_promocao = self.id_promocao_editada,
                nome=self.entry_nome.get(),
                desconto=self.entry_desconto.get(),
                data_inicio=self.entry_data_inicio.get(),
                data_fim=self.entry_data_fim.get()
            )
            self.promocao.atualizar_promocao(promocao)
            messagebox.showinfo("Sucesso", f"Promoção atualizada com sucesso!")
            self.carregar_promocoes()
            self.limpar_formulario()
                
    
            self.id_promocao_editada = None
        except Exception as e: 
            messagebox.showerror("Erro", str(e))
   
    def limpar_formulario(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_desconto.delete(0, tk.END)
        self.entry_data_inicio.delete(0, tk.END)
        self.entry_data_fim.delete(0, tk.END)
         
