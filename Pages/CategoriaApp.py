import tkinter as tk
from tkinter import ttk, messagebox
from Models.Categoria import CategoriaProduto
from DAL.categoria_dal import CategoriaDAL
from DB.DB_Utils import PG_DB_Utils as Database

class CategoriaApp:

    def __init__(self, parent, db):
        self.root = parent
        self.db = db
        self.categoria = CategoriaDAL(self.db)
        # Frame do formulário
        frame_form = tk.Frame(self.root, padx=10, pady=10)
        frame_form.pack(fill="x")

        # Labels e Entrys
        tk.Label(frame_form, text="Nome:").grid(row=0, column=0, sticky="w")
        self.entry_nome = tk.Entry(frame_form, width=50)
        self.entry_nome.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Descrição:").grid(row=1, column=0, sticky="w")
        self.entry_descricao = tk.Entry(frame_form, width=50)
        self.entry_descricao.grid(row=1, column=1, padx=5, pady=5)
        
        
        
        # Botão para adicionar cliente
        btn_add = tk.Button(frame_form, text="Adicionar Categoria", command=self.adicionar_categoria)
        btn_add.grid(row=6, column=0, pady=10)
        
        # Botão para editar cliente
        btn_add = tk.Button(frame_form, text="Editar Categoria", command=self.editar_categoria)
        btn_add.grid(row=6, column=1, pady=10)
        
        #Botão para remover cliente
        btn_add = tk.Button(frame_form, text="Remover Categoria", command=self.remover_categoria)
        btn_add.grid(row=6, column=2, pady=10)
        
        #Botão para guardar as alterações do botão editar
        btn_add = tk.Button(frame_form, text="Guardar Alterações", command=self.guardar_edicao)
        btn_add.grid(row=2, column=3, pady=5)
        
        
        # Tabela de clientes
        self.tree = ttk.Treeview(self.root, columns=("id", "nome", "descricao"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("descricao", text="Descrição")
        self.tree.column("id", width=50)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Carregar clientes existentes
        self.carregar_categoria()

    def adicionar_categoria(self):
        try:
            categoria = CategoriaProduto(
                nome=self.entry_nome.get(),
                descricao=self.entry_descricao.get(),
            )
            id_categoria = self.categoria.criarCategoria(categoria)
            messagebox.showinfo("Sucesso", f"Categoria criado com ID {id_categoria}")
            self.carregar_categoria()
            self.limpar_formulario()
        except Exception as e:
            messagebox.showerror("Erro", str(e))    


    def editar_categoria(self):
        try:
            if self.tree.focus():
                valores = self.tree.item(self.tree.focus(), "values")
                id_categoria = valores[0]
                
                self.id_categoria_editada= id_categoria

                self.entry_nome.delete(0, tk.END)
                self.entry_nome.insert(0, valores[1])

                self.entry_descricao.delete(0, tk.END)
                self.entry_descricao.insert(0, valores[2])
            else:
                messagebox.showerror("Aviso", "Selecione uma categoria!")
                return
  
        except Exception as e:
            messagebox.showerror("Erro", str(e))


    def remover_categoria(self):
        categoria_selecionada = self.tree.focus()
        if not self.tree.focus():
            messagebox.showerror("Aviso", "Selecione uma categoria primeiro!")
            return

        valores = self.tree.item(categoria_selecionada, "values")
        id_categoria = valores[0]

        confirm = messagebox.askyesno("Confirmar", f"Tem a certeza que deseja remover a categoria {valores[1]}?")
        if confirm:
            try:
                self.categoria.eliminarCategoria(id_categoria)
                self.tree.delete(categoria_selecionada)
                messagebox.showinfo("Sucesso", "Categoria removida com sucesso!")
                self.limpar_formulario()
            except Exception as e:
                messagebox.showerror("Error", f"Não foi possível remover a categoria: {e}")


    def carregar_categoria(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        categorias = self.categoria.obterTodasCategorias()
        for c in categorias:
            self.tree.insert("", "end", values=(c.id_categoria, c.nome, c.descricao))

    def guardar_edicao(self):
        if self.id_categoria_editada is None:
            messagebox.showerror("Erro", "Nenhuma categoria em edição.")
            return

        confirm = messagebox.askyesno("Aviso", "Deseja guardar as alterações?")
        if not confirm:
            return
            
        try:
            categoria = CategoriaProduto(
                id_categoria= self.id_categoria_editada,
                nome=self.entry_nome.get(),
                descricao=self.entry_descricao.get(),
            )
            self.categoria.atualizar_categoria(categoria)
            messagebox.showinfo("Sucesso", f"Categoria atualizada com sucesso!")
            self.carregar_categoria()
            self.limpar_formulario()
            
            
            self.id_categoria_editada = None
        except Exception as e: 
            messagebox.showerror("Erro", str(e))
   
    def limpar_formulario(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_descricao.delete(0, tk.END)

         
