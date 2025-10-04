import tkinter as tk 
from tkinter import ttk, messagebox 
from Models.Produto import Produto
from DAL.produto_dal import ProdutoDAL
from DB.DB_Utils import PG_DB_Utils as Database
from DAL.categoria_dal import CategoriaDAL


class ProdutoApp:

    def __init__(self, parent, db):
        self.root = parent
        self.db = db
        self.produto_dal = ProdutoDAL(self.db)
        self.categoria_dal = CategoriaDAL(self.db)
        self.categorias = self.categoria_dal.obterTodasCategorias()
        # Frame do formulário
        frame_form = tk.Frame(self.root, padx=10, pady=10)
        frame_form.pack(fill="x")

        # Labels e Entrys
        tk.Label(frame_form, text="Nome:").grid(row=0, column=0, sticky="w")
        self.entry_nome = tk.Entry(frame_form, width=50)
        self.entry_nome.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Preço:").grid(row=1, column=0, sticky="w")
        self.entry_preco = tk.Entry(frame_form, width=50)
        self.entry_preco.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Stock:").grid(row=2, column=0, sticky="w")
        self.entry_stock = tk.Entry(frame_form, width=50)
        self.entry_stock.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(frame_form, text="Categoria:").grid(row=3, column=0, sticky="w")
        self.entry_id_categoria = ttk.Combobox(frame_form, width=47)
        self.entry_id_categoria.grid(row=3, column=1, padx=5, pady=5)
        
        self.entry_id_categoria['values'] = [c.nome for c in self.categorias]

        # Botão para adicionar cliente
        btn_add = tk.Button(frame_form, text="Adicionar Produto", command=self.adicionar_produto)
        btn_add.grid(row=4, column=0, columnspan=1, pady=5, padx=5)
        
        # Botão para editar cliente
        btn_add = tk.Button(frame_form, text="Editar Produto", command=self.editar_produtos)
        btn_add.grid(row=4, column=1,  columnspan=1, pady=5)

        #Botão para remover cliente
        btn_add = tk.Button(frame_form, text="Remover Produto", command=self.remover_produto)
        btn_add.grid(row=4, column=2, pady=5)
        

        #Botão para guardar as alterações do botão editar
        btn_add = tk.Button(frame_form, text="Guardar Alterações", command=self.guardar_edicao)
        btn_add.grid(row=2, column=4, pady=5)
        
        
        # Tabela de clientes
        self.tree = ttk.Treeview(self.root, columns=("id", "nome","preco", "stock","categoria"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("preco", text="Preço")
        self.tree.heading("stock", text="Stock")
        self.tree.heading("categoria", text="Categoria")

        self.tree.column("id", width=50)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Carregar clientes existentes
        self.carregar_produtos()

    def adicionar_produto(self):
        try:
            id_categoria = self.get_categoria_id(self.entry_id_categoria.get())
            if not id_categoria:
                messagebox.showerror("Erro", "Categoria inválida.")
            
            produto = Produto(
                nome=self.entry_nome.get(),
                preco=self.entry_preco.get(),
                stock=self.entry_stock.get(),
                id_categoria=id_categoria
            )
            id_produto = self.produto_dal.criarProduto(produto)
            messagebox.showinfo("Sucesso", f"Cliente criado com ID {id_produto}")
            self.carregar_produtos()
            self.limpar_formulario()
        except Exception as e:
            messagebox.showerror("Erro", str(e))    


    def editar_produtos(self):
        try:
            if self.tree.focus():
                valores = self.tree.item(self.tree.focus(), "values")
                id_produto = valores[0]
                
                self.id_produto_editado= id_produto

                self.entry_nome.delete(0, tk.END)
                self.entry_nome.insert(0, valores[1])

                self.entry_preco.delete(0, tk.END)
                self.entry_preco.insert(0, valores[2])

                self.entry_stock.delete(0, tk.END)
                self.entry_stock.insert(0, valores[3])  
                                            
                self.entry_id_categoria.delete(0, tk.END)
                self.entry_id_categoria.insert(0, valores[4])  
                 
            else:
                messagebox.showerror("Aviso", "Selecione um produto!")
                return
  
        except Exception as e:
            messagebox.showerror("Erro", str(e))


    def remover_produto(self):
        produto_selecionado = self.tree.focus()
        if not self.tree.focus():
            messagebox.showerror("Aviso", "Selecione um produto primeiro!")
            return

        valores = self.tree.item(produto_selecionado, "values")
        id_produto = valores[0]

        confirm = messagebox.askyesno("Confirmar", f"Tem a certeza que deseja remover o produto {valores[1]}?")
        if confirm:
            try:
                self.produto_dal.eliminarProduto(id_produto)
                self.tree.delete(produto_selecionado)
                messagebox.showinfo("Sucesso", "Produto removido com sucesso!")
                self.limpar_formulario()
            except Exception as e:
                messagebox.showerror("Error", f"Não foi possível remover o produto: {e}")


    def carregar_produtos(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        produtos = self.produto_dal.obterTodosProdutos()
        for p in produtos:
            self.tree.insert("", "end", values=(p.id_produto, p.nome, p.preco, p.stock, p.id_categoria))



    def guardar_edicao(self):
        if self.id_produto_editado is None:
            messagebox.showerror("Erro", "Nenhum produto em edição.")
            return

        confirm = messagebox.askyesno("Aviso", "Deseja guardar as alterações?")
        if not confirm:
            return
            
        try:
            id_categoria = self.get_categoria_id(self.entry_id_categoria.get())
            if not id_categoria:
                messagebox.showerror("Erro", "Categoria inválida.")
            produto = Produto(
                id_produto = self.id_produto_editado,
                nome=self.entry_nome.get(),
                preco=self.entry_preco.get(),
                stock=self.entry_stock.get(),
                id_categoria=id_categoria
            )
            self.produto_dal.atualizar_produto(produto)
            messagebox.showinfo("Sucesso", f"Produto atualizado com sucesso!")
            self.carregar_produtos()
            self.limpar_formulario()
                
    
            self.id_produto_editado = None
        except Exception as e: 
            messagebox.showerror("Erro", str(e))
            
    def get_categoria_id(self, nome_categoria):
        for c in self.categorias:
            if c.nome == nome_categoria:
                return c.id_categoria  
        return None

   
    def limpar_formulario(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_preco.delete(0, tk.END)
        self.entry_stock.delete(0, tk.END)
        self.entry_id_categoria.delete(0, tk.END)
        

         
