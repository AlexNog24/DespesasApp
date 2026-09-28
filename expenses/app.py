import customtkinter as ctk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
import database
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Inicializar Base de Dados
database.init_db()

# Configuração da janela principal
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Gestor de Despesas e Poupanças")
        self.geometry("900x750")
        
        # Título
        self.title_label = ctk.CTkLabel(self, text="O Meu Gestor Financeiro", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.pack(pady=10)
        
        # Selector de Mês (Global)
        self.mes_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.mes_frame.pack(pady=5, padx=20, fill="x")
        
        ctk.CTkLabel(self.mes_frame, text="Mês de Visualização:", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=5)
        self.mes_var = ctk.StringVar()
        self.mes_menu = ctk.CTkOptionMenu(self.mes_frame, variable=self.mes_var, command=self.mudar_mes)
        self.mes_menu.pack(side="left", padx=5)
        
        # Tabview (Separadores)
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.tab_despesas = self.tabview.add("Despesas Diárias")
        self.tab_poupancas = self.tabview.add("Orçamento & Poupanças")
        
        # Inicializar meses
        self.atualizar_meses_disponiveis()
        
        self.setup_tab_despesas()
        self.setup_tab_poupancas()

    def atualizar_meses_disponiveis(self):
        meses = database.obter_meses_disponiveis()
        current_val = self.mes_var.get()
        if not current_val or current_val not in meses:
            self.mes_var.set(meses[0])
        self.mes_menu.configure(values=meses)

    def mudar_mes(self, selected_mes):
        self.atualizar_tabela()

    def setup_tab_despesas(self):
        # Frame de Entrada de Dados
        self.input_frame = ctk.CTkFrame(self.tab_despesas)
        self.input_frame.pack(pady=10, padx=10, fill="x")
        
        # Data
        self.data_label = ctk.CTkLabel(self.input_frame, text="Data (AAAA-MM-DD):")
        self.data_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.data_entry = ctk.CTkEntry(self.input_frame)
        self.data_entry.grid(row=0, column=1, padx=10, pady=10)
        self.data_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # Descrição
        self.desc_label = ctk.CTkLabel(self.input_frame, text="Descrição:")
        self.desc_label.grid(row=0, column=2, padx=10, pady=10, sticky="w")
        self.desc_entry = ctk.CTkEntry(self.input_frame, width=200)
        self.desc_entry.grid(row=0, column=3, padx=10, pady=10)
        
        # Categoria
        self.cat_label = ctk.CTkLabel(self.input_frame, text="Categoria:")
        self.cat_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.categorias = ["Alimentação", "Transporte", "Casa", "Lazer", "Saúde", "Educação", "Outros"]
        self.cat_menu = ctk.CTkOptionMenu(self.input_frame, values=self.categorias)
        self.cat_menu.grid(row=1, column=1, padx=10, pady=10)
        
        # Valor
        self.valor_label = ctk.CTkLabel(self.input_frame, text="Valor (€):")
        self.valor_label.grid(row=1, column=2, padx=10, pady=10, sticky="w")
        self.valor_entry = ctk.CTkEntry(self.input_frame)
        self.valor_entry.grid(row=1, column=3, padx=10, pady=10)
        
        # Botão Adicionar
        self.add_btn = ctk.CTkButton(self.input_frame, text="Adicionar Despesa", command=self.adicionar_despesa, font=ctk.CTkFont(weight="bold"))
        self.add_btn.grid(row=2, column=0, columnspan=4, pady=10)
        
        # Frame de Tabela
        self.table_frame = ctk.CTkFrame(self.tab_despesas)
        self.table_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Estilo da Tabela
        style = ttk.Style()
        style.theme_use("default")
        
        bg_color = self._apply_appearance_mode(ctk.ThemeManager.theme["CTkFrame"]["fg_color"])
        text_color = self._apply_appearance_mode(ctk.ThemeManager.theme["CTkLabel"]["text_color"])
        selected_color = self._apply_appearance_mode(ctk.ThemeManager.theme["CTkButton"]["fg_color"])
        
        style.configure("Treeview", background=bg_color, foreground=text_color, rowheight=30, fieldbackground=bg_color, font=("Helvetica", 11))
        style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))
        style.map('Treeview', background=[('selected', selected_color)])
        
        self.tree = ttk.Treeview(self.table_frame, columns=("ID", "Data", "Descrição", "Categoria", "Valor"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Data", text="Data")
        self.tree.heading("Descrição", text="Descrição")
        self.tree.heading("Categoria", text="Categoria")
        self.tree.heading("Valor", text="Valor (€)")
        
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Data", width=120, anchor="center")
        self.tree.column("Descrição", width=300, anchor="w")
        self.tree.column("Categoria", width=150, anchor="center")
        self.tree.column("Valor", width=120, anchor="e")
        
        self.tree.pack(fill="both", expand=True, side="left")
        
        scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Frame inferior para total e apagar
        self.bottom_frame = ctk.CTkFrame(self.tab_despesas, fg_color="transparent")
        self.bottom_frame.pack(pady=10, padx=10, fill="x")
        
        self.total_label = ctk.CTkLabel(self.bottom_frame, text="Total: 0.00 €", font=ctk.CTkFont(size=18, weight="bold"))
        self.total_label.pack(side="left")
        
        self.graph_btn = ctk.CTkButton(self.bottom_frame, text="Ver Gráfico", command=self.mostrar_grafico)
        self.graph_btn.pack(side="left", padx=20)
        
        self.del_btn = ctk.CTkButton(self.bottom_frame, text="Apagar Selecionada", command=self.apagar_despesa, fg_color="#b00020", hover_color="#7a0016")
        self.del_btn.pack(side="right")
        
        self.atualizar_tabela()

    def setup_tab_poupancas(self):
        # Dividir em duas colunas: Esquerda (Adicionar) e Direita (Resumo/Poupança)
        self.orc_left = ctk.CTkFrame(self.tab_poupancas)
        self.orc_left.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        self.orc_right = ctk.CTkFrame(self.tab_poupancas)
        self.orc_right.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        # --- ESQUERDA: Adicionar Rendimento / Despesa Fixa ---
        ctk.CTkLabel(self.orc_left, text="Adicionar ao Orçamento", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
        
        self.orc_nome_entry = ctk.CTkEntry(self.orc_left, placeholder_text="Nome (ex: Salário, Renda)")
        self.orc_nome_entry.pack(pady=10, padx=20, fill="x")
        
        self.orc_tipo_menu = ctk.CTkOptionMenu(self.orc_left, values=["Rendimento", "Despesa Fixa"])
        self.orc_tipo_menu.pack(pady=10, padx=20, fill="x")
        
        self.orc_valor_entry = ctk.CTkEntry(self.orc_left, placeholder_text="Valor (€)")
        self.orc_valor_entry.pack(pady=10, padx=20, fill="x")
        
        self.orc_add_btn = ctk.CTkButton(self.orc_left, text="Adicionar", command=self.adicionar_orcamento)
        self.orc_add_btn.pack(pady=15)
        
        # Tabela de Orçamento
        self.orc_tree = ttk.Treeview(self.orc_left, columns=("ID", "Nome", "Tipo", "Valor"), show="headings", height=8)
        self.orc_tree.heading("ID", text="ID")
        self.orc_tree.heading("Nome", text="Nome")
        self.orc_tree.heading("Tipo", text="Tipo")
        self.orc_tree.heading("Valor", text="Valor (€)")
        self.orc_tree.column("ID", width=30, anchor="center")
        self.orc_tree.column("Nome", width=120, anchor="w")
        self.orc_tree.column("Tipo", width=100, anchor="center")
        self.orc_tree.column("Valor", width=80, anchor="e")
        self.orc_tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.orc_del_btn = ctk.CTkButton(self.orc_left, text="Apagar Selecionada", command=self.apagar_orcamento, fg_color="#b00020", hover_color="#7a0016")
        self.orc_del_btn.pack(pady=10)
        
        # --- DIREITA: Resumo e Poupança ---
        ctk.CTkLabel(self.orc_right, text="Resumo Mensal", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)
        
        self.resumo_rendimentos = ctk.CTkLabel(self.orc_right, text="Rendimentos Totais: 0.00 €", font=ctk.CTkFont(size=16), text_color="green")
        self.resumo_rendimentos.pack(pady=10)
        
        self.resumo_fixas = ctk.CTkLabel(self.orc_right, text="Despesas Fixas Totais: 0.00 €", font=ctk.CTkFont(size=16), text_color="#d9534f")
        self.resumo_fixas.pack(pady=10)
        
        self.resumo_diarias = ctk.CTkLabel(self.orc_right, text="Despesas Diárias (Mês): 0.00 €", font=ctk.CTkFont(size=16), text_color="#d9534f")
        self.resumo_diarias.pack(pady=10)
        
        ctk.CTkFrame(self.orc_right, height=2, fg_color="gray").pack(fill="x", padx=40, pady=20)
        
        self.resumo_poupanca = ctk.CTkLabel(self.orc_right, text="Poupança Estimada: 0.00 €", font=ctk.CTkFont(size=20, weight="bold"))
        self.resumo_poupanca.pack(pady=10)
        
        self.atualizar_orcamento()

    # --- FUNÇÕES DESPESAS DIÁRIAS ---
    def adicionar_despesa(self):
        data = self.data_entry.get()
        desc = self.desc_entry.get()
        cat = self.cat_menu.get()
        valor_str = self.valor_entry.get()
        
        if not data or not desc or not valor_str:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
            return
            
        try:
            valor = float(valor_str.replace(",", "."))
        except ValueError:
            messagebox.showerror("Erro", "O valor tem de ser um número válido.")
            return
            
        database.adicionar_despesa(data, desc, cat, valor)
        
        self.desc_entry.delete(0, ctk.END)
        self.valor_entry.delete(0, ctk.END)
        
        self.atualizar_meses_disponiveis()
        
        # Mudar a vista para o mês da despesa acabada de inserir
        added_month = data[:7]
        if added_month in self.mes_menu.cget("values"):
            self.mes_var.set(added_month)
            
        self.atualizar_tabela()

    def atualizar_tabela(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        mes_atual = self.mes_var.get()
        despesas = database.obter_despesas_mes(mes_atual)
        total = 0
        for d in despesas:
            self.tree.insert("", "end", values=(d[0], d[1], d[2], d[3], f"{d[4]:.2f}"))
            total += d[4]
            
        self.total_label.configure(text=f"Total: {total:.2f} €")
        
        # Atualizar resumo sempre que as despesas mudam
        if hasattr(self, 'orc_tree'):
            self.atualizar_resumo()

    def apagar_despesa(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Aviso", "Por favor, selecione uma despesa na tabela para apagar.")
            return
            
        item = self.tree.item(selected_item)
        id_despesa = item['values'][0]
        
        database.apagar_despesa(id_despesa)
        
        self.atualizar_meses_disponiveis()
        self.atualizar_tabela()

    def mostrar_grafico(self):
        mes_atual = self.mes_var.get()
        dados = database.total_por_categoria_mes(mes_atual)
        
        if not dados:
            messagebox.showinfo("Aviso", f"Não existem dados para mostrar no gráfico para {mes_atual}.")
            return
            
        categorias = [d[0] for d in dados]
        valores = [d[1] for d in dados]
        
        janela_grafico = ctk.CTkToplevel(self)
        janela_grafico.title(f"Despesas por Categoria - {mes_atual}")
        janela_grafico.geometry("600x500")
        
        fig, ax = plt.subplots(figsize=(6, 5))
        ax.pie(valores, labels=categorias, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        
        canvas = FigureCanvasTkAgg(fig, master=janela_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    # --- FUNÇÕES ORÇAMENTO E POUPANÇA ---
    def adicionar_orcamento(self):
        nome = self.orc_nome_entry.get()
        tipo = self.orc_tipo_menu.get()
        valor_str = self.orc_valor_entry.get()
        
        if not nome or not valor_str:
            messagebox.showerror("Erro", "Preencha o nome e o valor.")
            return
            
        try:
            valor = float(valor_str.replace(",", "."))
        except ValueError:
            messagebox.showerror("Erro", "O valor tem de ser um número válido.")
            return
            
        database.adicionar_orcamento(nome, tipo, valor)
        
        self.orc_nome_entry.delete(0, ctk.END)
        self.orc_valor_entry.delete(0, ctk.END)
        
        self.atualizar_orcamento()

    def atualizar_orcamento(self):
        for item in self.orc_tree.get_children():
            self.orc_tree.delete(item)
            
        orcamentos = database.obter_orcamento()
        for o in orcamentos:
            self.orc_tree.insert("", "end", values=(o[0], o[1], o[2], f"{o[3]:.2f}"))
            
        self.atualizar_resumo()

    def apagar_orcamento(self):
        selected_item = self.orc_tree.selection()
        if not selected_item:
            messagebox.showwarning("Aviso", "Selecione um item na tabela para apagar.")
            return
            
        item = self.orc_tree.item(selected_item)
        id_orcamento = item['values'][0]
        
        database.apagar_orcamento(id_orcamento)
        self.atualizar_orcamento()

    def atualizar_resumo(self):
        mes_atual = self.mes_var.get()
        orcamentos = database.obter_orcamento()
        despesas_diarias_totais = sum([d[4] for d in database.obter_despesas_mes(mes_atual)])
        
        rendimentos = sum([o[3] for o in orcamentos if o[2] == "Rendimento"])
        despesas_fixas = sum([o[3] for o in orcamentos if o[2] == "Despesa Fixa"])
        
        poupanca = rendimentos - despesas_fixas - despesas_diarias_totais
        
        try:
            self.resumo_rendimentos.configure(text=f"Rendimentos Totais: {rendimentos:.2f} €")
            self.resumo_fixas.configure(text=f"Despesas Fixas Totais: {despesas_fixas:.2f} €")
            self.resumo_diarias.configure(text=f"Despesas Diárias ({mes_atual}): {despesas_diarias_totais:.2f} €")
            self.resumo_poupanca.configure(text=f"Poupança Estimada: {poupanca:.2f} €")
            
            if poupanca > 0:
                self.resumo_poupanca.configure(text_color="green")
            elif poupanca < 0:
                self.resumo_poupanca.configure(text_color="#d9534f")
            else:
                self.resumo_poupanca.configure(text_color="gray")
        except AttributeError:
            pass

if __name__ == "__main__":
    app = App()
    app.mainloop()

