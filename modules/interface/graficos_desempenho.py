import customtkinter as ctk
import matplotlib.pyplot as plt
from modules.interface import dashboard
from modules.data import json_handler
from tkinter import messagebox
from tkinterweb import HtmlFrame  # Certifique-se de ter o tkinterweb instalado

def fechar_programa(root):
    root.quit()  # Encerra qualquer execução que esteja pendente
    root.destroy()  # Fecha a janela do Tkinter corretamente

def tela_desempenho(root, frame_, matricula):
    # Limpa a tela
    for widget in root.winfo_children():
        widget.destroy()

    # Cores principais
    cor_principal = "#2e8b57"  # Verde
    cor_secundaria = "#4682b4"
    cor_erro = "#ff6347"  # Vermelho
    cor_barra_erro = "#ff0000"  # Vermelho para notas abaixo de 70
    cor_barra_normal = "#1e90ff"  # Azul para notas acima de 70

    # Carregar dados do aluno
    try:
        dados = json_handler.carregar_dados()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao carregar os dados: {e}")
        return

    aluno = dados['alunos'].get(matricula)
    if not aluno:
        messagebox.showerror("Erro", "Aluno não encontrado.")
        return

    cursos = aluno.get('cursos', {})

    # Frame principal
    frame_principal = ctk.CTkFrame(root, corner_radius=10)
    frame_principal.place(relx=0.5, rely=0.5, relwidth=0.85, relheight=0.85, anchor='center')

    # Título
    label_titulo = ctk.CTkLabel(
        frame_principal, text=f"Desempenho de {aluno['nome']}", 
        font=("Arial", 22, "bold"), text_color=cor_principal
    )
    label_titulo.pack(pady=15)

    # Função para exibir gráfico de desempenho
    def atualizar_grafico():
        # Remove gráficos antigos
        for widget in frame_graficos.winfo_children():
            widget.destroy()

        curso_selecionado = curso_var.get()
        if curso_selecionado == "Selecione um curso":
            messagebox.showinfo("Erro", "Por favor, selecione um curso primeiro.")
            return

        id_curso = [cid for cid in cursos if dados['cursos'][cid]['nome'] == curso_selecionado][0]
        curso = dados['cursos'][id_curso]
        disciplinas_curso = curso['id_disciplinas']

        disciplinas_nomes = []
        notas_aluno = []

        # Prepara os dados de desempenho
        for id_disciplina in disciplinas_curso:
            disciplina = dados['disciplinas'][id_disciplina]
            disciplinas_nomes.append(disciplina['nome'])
            notas = dados['notas'][matricula].get(id_disciplina, [0, 0])
            media_aluno = sum(notas) / len(notas) if notas else 0
            notas_aluno.append(media_aluno)

        if not disciplinas_nomes:
            messagebox.showinfo("Erro", "Nenhuma disciplina encontrada para o curso selecionado.")
            return

        # Usando matplotlib para gerar o gráfico
        fig, ax = plt.subplots(figsize=(6, 4))  # Ajuste do tamanho do gráfico para caber melhor na tela

        barras = []
        for i, nota in enumerate(notas_aluno):
            # Verifica se a nota é menor que 70 e define a cor
            cor_barra = cor_barra_normal if nota >= 70 else cor_barra_erro
            barra = ax.bar(disciplinas_nomes[i], nota, color=cor_barra)
            barras.append(barra)

            # Adiciona a média da nota sobre cada barra
            ax.text(
                barra.get_x() + barra.get_width() / 2,  # X da barra (meio)
                barra.get_height() + 2,  # Coloca o texto um pouco acima da barra
                f'{nota:.2f}',  # Exibe a média com 2 casas decimais
                ha='center',  # Alinha o texto no centro
                va='bottom',  # Alinha o texto acima da barra
                fontsize=10  # Tamanho da fonte do texto
            )

        ax.set_title(f"Desempenho em {curso['nome']}", fontsize=12)  # Título menor
        ax.set_xlabel("Disciplinas", fontsize=10)  # Fonte menor
        ax.set_ylabel("Nota", fontsize=10)  # Fonte menor
        ax.set_ylim(0, 100)  # Ajuste o eixo Y para o intervalo de notas (0 a 100)

        # Ajuste do layout para garantir que os nomes das disciplinas não fiquem cortados
        plt.xticks(rotation=45, ha='right', fontsize=8)  # Ajuste da fonte para os rótulos das disciplinas
        plt.yticks(fontsize=8)  # Ajuste da fonte para os rótulos do eixo Y
        fig.tight_layout()  # Ajusta automaticamente o layout para evitar cortes

        # Exibe o gráfico
        canvas = ctk.CTkCanvas(frame_graficos)
        canvas.pack(expand=True, fill='both', padx=15, pady=10)
        
        # Converte o gráfico do Matplotlib para o Tkinter
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        figure_canvas = FigureCanvasTkAgg(fig, master=canvas)
        figure_canvas.draw()
        figure_canvas.get_tk_widget().pack(fill='both', expand=True)

    # ComboBox de cursos
    curso_var = ctk.StringVar(value="Selecione um curso")

    # Função para filtrar cursos e atualizar gráficos
    dropdown_cursos = ctk.CTkOptionMenu(
        frame_principal, variable=curso_var, 
        values=[dados['cursos'][cid]['nome'] for cid in cursos],
        command=lambda _: atualizar_grafico()
    )
    dropdown_cursos.pack(pady=10)

    # Frame para gráficos
    frame_graficos = ctk.CTkFrame(frame_principal)
    frame_graficos.pack(expand=True, fill='both')

    # Botão de Voltar
    button_voltar = ctk.CTkButton(
        root, text="Voltar", 
        font=("Arial", 18, "bold"),
        hover_color=cor_principal,
        command=lambda: dashboard.exibir_dashboard(root, matricula)
    )
    button_voltar.place(relx=0.15, rely=0.96, anchor='center')

    # Ao fechar, chamamos a função de limpar na janela principal
    root.protocol("WM_DELETE_WINDOW", lambda: fechar_programa(root))
