import tkinter as tk
from tkinter import ttk, messagebox
from Models.Encomenda import Encomenda
from DAL.encomenda_dal import EncomendaDAL
from DAL.produto_dal import ProdutoDAL
from DB.DB_Utils import PG_DB_Utils as Database
from DAL.cliente_dal import ClienteDAL
from DAL.fatura_dal import FaturaDAL
import datetime 
from DAL.promocao_dal import PromocaoDAL
import math



class EncomendaApp:

    def __init__(self, parent, db):
        self.root = parent
        self.db = db
        self.encomenda_dal = EncomendaDAL(self.db)
        self.produto_dal = ProdutoDAL(self.db)
        self.produto = self.produto_dal.obterTodosProdutos()
        self.cliente_dal = ClienteDAL(self.db)
        self.cliente = self.cliente_dal.obterTodosClientes()
        self.id_encomenda_editada = None
        self.fatura_dal = FaturaDAL(self.db)
        self.fatura = self.fatura_dal.obterTodasFaturas()
        self.promocao_dal = PromocaoDAL(self.db)
        self.obter_promocao = self.promocao_dal.obterTodasPromocoes()
        self.promocao = self.promocao_dal.verificar_promocao()
    
        frame_form = tk.Frame(self.root, padx=10, pady=10)
        frame_form.pack(fill="x")

        # Labels e Entrys
        tk.Label(frame_form, text="Cliente:").grid(row=0, column=0, sticky="w")
        self.entry_id_cliente = ttk.Combobox(frame_form, width=50)
        self.entry_id_cliente.grid(row=0, column=1, padx=5, pady=5)
        self.entry_id_cliente['values'] = [c.nome for c in self.cliente]

        tk.Label(frame_form, text="Produto/s:").grid(row=1, column=0, sticky="w")
        self.entry_id_produto = tk.Listbox(frame_form, width=50, selectmode=tk.MULTIPLE)
        self.entry_id_produto.grid(row=1, column=1, padx=5, pady=5)
        for p in self.produto:
            self.entry_id_produto.insert("end", p.nome)
        

        tk.Label(frame_form, text="Quantidade:").grid(row=2, column=0, sticky="w")
        self.entry_quantidade = tk.Entry(frame_form, width=50)
        self.entry_quantidade.grid(row=2, column=1, padx=15, pady=5)
        
        tk.Label(frame_form, text="Data Entrega:").grid(row=3, column=0, sticky="w")
        self.entry_data = tk.Entry(frame_form, width=50)
        self.entry_data.grid(row=3, column=1, padx=5, pady=5)
        
        tk.Label(frame_form, text="Estado:").grid(row=4, column=0, sticky="w")
        self.entry_estado = ttk.Combobox(frame_form, width=47)
        self.entry_estado.grid(row=4, column=1, padx=5, pady=5)
        self.entry_estado['values'] = ["Pendente", "Concluída", "Cancelada"]
        

        # Botão para adicionar encomenda
        btn_adicionar = tk.Button(frame_form, text="Adicionar Encomenda", command=self.adicionar_encomenda, width=17, bg="white", height=1)
        btn_adicionar.grid(row=5, column=0, columnspan=1, pady=5, padx=5)

        #Botão para remover a encomenda
        btn_remover = tk.Button(frame_form, text="Remover Encomenda", command=self.remover_encomenda, width=17, bg="white", height=1)
        btn_remover.grid(row=5, column=1, columnspan=1, pady=5)
        
        btn_fatura = tk.Button(frame_form, text="Fatura", command=self.mostrar_fatura, width=10, bg="white", height=1)
        btn_fatura.grid(row=1, column=2, pady=5)
        
        btn_editar= tk.Button(frame_form, text="Alterar Estado", command=self.mudar_estado, width=14, bg="white", height=1)
        btn_editar.grid(row=2, column=2, pady=5)
        
        
        # Tabela de clientes
        self.tree = ttk.Treeview(self.root, columns=("id", "cliente", "data_encomenda", "estado"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("cliente", text="Cliente")
        self.tree.heading("data_encomenda", text="Data Entrega")
        self.tree.heading("estado", text="Estado")

        self.tree.column("id", width=50)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.tree.bind("<Double-1>", self.janela_informacoes_encomenda)

        # Carregar as encomendas existentes
        self.carregar_encomendas()

    def adicionar_encomenda(self):
        try:
            id_cliente = self.get_id_cliente(self.entry_id_cliente.get())
            if not id_cliente:
                messagebox.showerror("Erro", "Cliente inválido.")
                return
 
            escolha_estado = self.get_escolha_estado(self.entry_estado.get())
            if not escolha_estado:
                messagebox.showerror("Erro", "Estado inválido.")
                return
        
            encomenda = Encomenda(
                id_cliente=id_cliente, 
                data_encomenda=self.entry_data.get(),
                estado=escolha_estado
            )

            id_encomenda = self.encomenda_dal.criarEncomenda(encomenda)
            encomenda.id_encomenda = id_encomenda

            produto_selecionado = self.entry_id_produto.curselection()
            quantidade = self.entry_quantidade.get().split(",")
            
            if len(produto_selecionado) != len(quantidade):
                messagebox.showerror("Erro", "A quantidade dos produtos não corresponde ao número de produtos selecionados.")
                return

            for i in range(len(produto_selecionado)):
                produto = self.produto[produto_selecionado[i]]
                produto.id_encomenda = id_encomenda
                produto.quantidade = int(quantidade[i].strip())
                self.encomenda_dal.criarEncomendaProdutos(produto)
        
            messagebox.showinfo("Sucesso", f"Encomenda criada com ID {id_encomenda}")
            self.carregar_encomendas()
            self.limpar_formulario()
        except Exception as e:
            messagebox.showerror("Erro", str(e))    

    def remover_encomenda(self):
        encomenda_selecionada = self.tree.focus()
        if not self.tree.focus():
            messagebox.showerror("Aviso", "Selecione uma Encomenda primeiro!")
            return

        valores = self.tree.item(encomenda_selecionada, "values")
        id_encomenda = valores[0]

        confirm = messagebox.askyesno("Confirmar", f"Tem a certeza que deseja remover a encomenda com o ID {valores[0]}?")
        if confirm:
            try:
                self.encomenda_dal.eliminarEncomenda(id_encomenda)
                self.tree.delete(encomenda_selecionada)
                messagebox.showinfo("Sucesso", "Encomenda removida com sucesso!")
                self.limpar_formulario()
            except Exception as e:
                messagebox.showerror("Error", f"Não foi possível remover a encomenda: {e}")


    def carregar_encomendas(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        encomendas = self.encomenda_dal.obterTodasEncomendas()
        
        for e in encomendas:
            self.tree.insert("", "end", values=(e.id_encomenda, e.id_cliente, e.data_encomenda, e.estado))
            
    def guardar_edicao(self):
        if self.id_encomenda_editada is None:
            messagebox.showerror("Erro", "Nenhuma encomenda em edição.")
            return

        confirm = messagebox.askyesno("Aviso", "Deseja guardar as alterações?")
        if not confirm:
            return
            
        try:              
            estado_escolhido = self.get_escolha_estado(self.entry_novo_estado.get())
            if not estado_escolhido:
                messagebox.showerror("Erro", "Estado inválido.")  
                
                
            encomenda = Encomenda(
                id_encomenda= self.id_encomenda_editada,
                estado=self.entry_novo_estado.get()
            )
            self.encomenda_dal.atualizarEncomenda(encomenda)
            messagebox.showinfo("Sucesso", f"Encomenda foi atualizada com sucesso!")

            
            self.carregar_encomendas()
            self.limpar_formulario()
            self.nova_janela.destroy()

            self.id_encomenda_editada = None
        except Exception as e: 
            messagebox.showerror("Erro", str(e))
            
    def get_id_cliente(self, nome_cliente):
        for c in self.cliente:
            if c.nome == nome_cliente:
                return c.id_pessoa  
        return None
    
    def get_id_produto(self, nome_produto):
        for p in self.produto:
            if p.nome == nome_produto:
                return p.id_produto  
        return None
    
    def get_escolha_estado(self, nome_estado):
        estados=["Pendente", "Concluída", "Cancelada"]
        if nome_estado in estados:
            return nome_estado    
        return None
    
    def get_id_encomenda(self, id_encomenda):
        encomendas = self.encomenda_dal.obterTodasEncomendas()
        for e in encomendas:
            if e.id_encomenda == id_encomenda:
                return e
        return None
    
    def obterFaturaEncomenda(self, id_encomenda):
        faturas = self.fatura_dal.obterTodasFaturas()
        for f in faturas:
            if f.id_encomenda == id_encomenda:
                return f
        return None


    def limpar_formulario(self):
        self.entry_id_cliente.delete(0, tk.END)
        self.entry_quantidade.delete(0, tk.END)
        self.entry_data.delete(0, tk.END)
        self.entry_estado.delete(0, tk.END)
        
    def janela_informacoes_encomenda(self, event):
        encomenda_selecionada = self.tree.selection()
        if encomenda_selecionada:
           
            item = encomenda_selecionada[0]
            valores = self.tree.item(item, "values")
            id_encomenda = valores[0]
        
            nova_janela = tk.Toplevel(self.root)
            nova_janela.title(f"Informações da Encomenda")
            self.tree_produtos = ttk.Treeview(nova_janela, columns=("id", "produtos", "quantidade", "preco", "preco_total"), show="headings")
            self.tree_produtos.heading("id", text="ID")
            self.tree_produtos.heading("produtos", text="Produtos")
            self.tree_produtos.heading("quantidade", text="Quantidade")
            self.tree_produtos.heading("preco", text="Preço unitário")
            self.tree_produtos.heading("preco_total", text="Preço total")
            self.tree_produtos.column("id", width=50)
            self.tree_produtos.pack(fill="both", expand=True, padx=10, pady=10)
        
        
            self.carregar_informacoes(id_encomenda, self.tree_produtos)
        
        else:
            messagebox.showerror("Aviso", "Selecione uma Encomenda primeiro!") 
            return
        
    def carregar_informacoes(self, id_encomenda, tree_produtos):
        for i in tree_produtos.get_children():
            tree_produtos.delete(i)

        produtos = self.encomenda_dal.obterTodosProdutos(id_encomenda)
        print("Produtos para a encomenda", id_encomenda, ":", produtos)

        for p in produtos:
            preco_total = p.quantidade * p.preco
            tree_produtos.insert("", "end", values=(p.id_produto, p.nome, p.quantidade, p.preco, preco_total))
            
            
            
    def mudar_estado(self):
        encomenda_selecionada = self.tree.selection()
        if not encomenda_selecionada:
            messagebox.showerror("Erro", "Para executar este comando tem de selecionar primeiro uma encomenda.")
            return
        
            
        item = encomenda_selecionada[0]
        valores = self.tree.item(item, "values")
        self.id_encomenda_editada = valores[0]
        estado = valores[3]
        
        self.nova_janela = tk.Toplevel(self.root)
        self.nova_janela.title(f"Alteração do estado")
        self.nova_janela.geometry("450x250")
        
        tk.Label(self.nova_janela, text="Novo Estado:").grid(row=1, column=0, sticky="w")
        self.entry_novo_estado = ttk.Combobox(self.nova_janela, width=47)
        self.entry_novo_estado.grid(row=1, column=1, padx=10, pady=10)
        self.entry_novo_estado['values'] = ["Pendente", "Concluída", "Cancelada"]
        self.entry_novo_estado.set(estado)
            
        btn_guardar = tk.Button(self.nova_janela, text="Guardar Alterações", command=self.guardar_edicao)
        btn_guardar.grid(row=2, column=1, pady=20)
        
        
        
    def mostrar_fatura(self):
        encomenda_selecionada = self.tree.selection()
        if not encomenda_selecionada:
            messagebox.showerror("Erro", "Para executar este comando tem de selecionar primeiro uma encomenda.")
            return
        
        item = encomenda_selecionada[0]
        valores = self.tree.item(item, "values")
        self.id_encomenda_editada = valores[0]
        

        encomenda = self.get_id_encomenda(self.id_encomenda_editada)
        produtos = self.encomenda_dal.obterTodosProdutos(self.id_encomenda_editada)
      
        self.janela_fatura = tk.Toplevel(self.root)
        self.janela_fatura.title(f"Fatura")
        self.janela_fatura.geometry("700x400")


        self.tree_fatura = ttk.Treeview(self.janela_fatura, columns=("id", "data_emissao", "nome", "quantidade", "preco", "preco_total", "promocao","valor_total"), show="headings")
        self.tree_fatura.heading("id", text="ID")
        self.tree_fatura.heading("data_emissao", text="Data Emissão")
        self.tree_fatura.heading("nome", text="Nome")
        self.tree_fatura.heading("quantidade", text="Quantidade")
        self.tree_fatura.heading("preco", text="Preço unitário")
        self.tree_fatura.heading("preco_total", text="Preço total")
        self.tree_fatura.heading("promocao", text="Promoção")
        self.tree_fatura.heading("valor_total", text="Valor Acumulado")
        self.tree_fatura.column("id", width=50)
        self.tree_fatura.pack(fill="both", expand=True, padx=10, pady=10)
       
       
        valor_total=0
        for p in produtos:
            preco_total = p.quantidade * p.preco
            for promo in self.obter_promocao:
                desconto = promo.desconto
                break
            valor_desconto = (preco_total * desconto / 100)
            preco_com_desconto = preco_total - valor_desconto
            valor_total += round(preco_com_desconto, 2)
            data_hora_agora = datetime.datetime.now()
            self.data_emissao = data_hora_agora.strftime("%d/%m/%Y %H:%M:%S")
            self.tree_fatura.insert("", "end", values=(p.id_produto, self.data_emissao, p.nome, p.quantidade, p.preco, preco_total, desconto, valor_total))
  
        btn_imprimir_fatura = tk.Button(self.janela_fatura, text="Imprimir", command=self.imprimir_fatura)
        btn_imprimir_fatura.pack(pady=5)
  
    def imprimir_fatura(self):
        with open("Fatura.txt", "w") as fatura:
            fatura.write("  Fatura  \n".center(50))
            fatura.write(f"Data Emissão: {self.data_emissao}\n")
            fatura.write("---------------------------------------------------------------\n")
            fatura.write("Quantidade |        Produtos         |  Preço Unitário \n")
            for item in self.tree_fatura.get_children():
                informacoes = self.tree_fatura.item(item, "values")
                fatura.write(f"{informacoes[3]} |  {informacoes[2]}  |   {informacoes[4]}\n")
                fatura.write("---------------------------------------------------------------\n")
            fatura.write(f"Preço Total: {informacoes[5]}\n")
            fatura.write(f"Desconto: {informacoes[6]}\n")
            fatura.write(f"Valor Total: {informacoes[7]}\n") 
            fatura.write("\n")
            fatura.write("\n")
            
            fatura.write("--------------------------------------\n")
            fatura.write("      Obrigado pela Preferência     \n")
            fatura.write("--------------------------------------\n")
            
            messagebox.showinfo("Concluído", "A fatura foi imprimida com sucesso!")
            
            fatura.close()
        
        
        
        