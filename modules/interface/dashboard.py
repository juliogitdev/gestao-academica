import customtkinter as ctk
from modules.data import json_handler
from modules.interface import cursos, disciplinas, notas, historico_academico, graficos_desempenho, perfil
from api import api_handler

def exibir_dashboard(root, matricula):
    # Limpar widgets existentes
    for widget in root.winfo_children():
        widget.destroy()

    # Carregar dados
    dados = json_handler.carregar_dados()
    dados_aluno = dados['alunos'][matricula]
    id_disciplinas = dados_aluno['disciplinas']

    cor_verde = "#2e8b57"

    # Tela principal (dashboard)
    tela_dashboard = ctk.CTkFrame(root)
    tela_dashboard.pack(fill="both", expand=True)

    # Frame para título
    frame_titulo = ctk.CTkFrame(tela_dashboard, corner_radius=0)
    frame_titulo.place(relx=0, rely=0, relwidth=1, relheight=0.1)

    # Texto "SISTEMA DE GESTÃO ACADÊMICA"
    label_gestao_academica = ctk.CTkLabel(
        frame_titulo,
        font=('Arial', 30, 'bold'),
        text="SISTEMA DE GESTÃO ACADÊMICA",
        text_color=cor_verde
    )
    label_gestao_academica.place(relx=0.5, rely=0.5, anchor='center')

    # Frame para os botões de navegação (menu)
    frame_nav = ctk.CTkFrame(tela_dashboard, corner_radius=0, fg_color="transparent")
    frame_nav.place(relx=0, rely=0.1, relwidth=1, relheight=0.05)

    # Botões de navegação (organizados em colunas)
    button_cursos = ctk.CTkButton(
        frame_nav,
        text='Cursos',
        font=('Arial', 15, 'bold'),
        fg_color="transparent",  # Remove a cor de fundo
        hover_color=cor_verde,   # Cor ao passar o mouse
        command=lambda: cursos.tela_cursos(root, matricula)
    )
    button_cursos.grid(row=0, column=0, sticky="nsew")

    button_disciplinas = ctk.CTkButton(
        frame_nav,
        text='Disciplinas',
        font=('Arial', 15, 'bold'),
        fg_color="transparent",  # Remove a cor de fundo
        hover_color=cor_verde,   # Cor ao passar o mouse
        command=lambda: disciplinas.mostrar_disciplinas(root, matricula)
    )
    button_disciplinas.grid(row=0, column=1, sticky="nsew")

    button_notas = ctk.CTkButton(
        frame_nav,
        text='Notas',
        font=('Arial', 15, 'bold'),
        fg_color="transparent",  # Remove a cor de fundo
        hover_color=cor_verde,   # Cor ao passar o mouse
        command=lambda: notas.mostrar_notas(root, matricula)
    )
    button_notas.grid(row=0, column=2, sticky="nsew")

    button_desempenho = ctk.CTkButton(
        frame_nav,
        text='Desempenho',
        font=('Arial', 15, 'bold'),
        fg_color="transparent",
        hover_color=cor_verde,
        command=lambda: graficos_desempenho.tela_desempenho(root, frame_conteudo, matricula)  # Passe o root, não frame_conteudo
    )
    button_desempenho.grid(row=0, column=3, sticky="nsew")

    button_perfil = ctk.CTkButton(
        frame_nav,
        text='Perfil',
        font=('Arial', 15, 'bold'),
        fg_color="transparent",  # Remove a cor de fundo
        hover_color=cor_verde,
        command=lambda: perfil.tela_perfil(root, matricula)
    )
    button_perfil.grid(row=0, column=4, sticky="nsew")

    # Configuração das colunas para expandir igualmente
    for i in range(5):  # 5 colunas (uma para cada botão)
        frame_nav.grid_columnconfigure(i, weight=1)

    # Frame para conteúdo (lado direito)
    frame_direito = ctk.CTkFrame(tela_dashboard, fg_color='transparent')
    frame_direito.place(relwidth=1, relheight=0.85, rely=0.15)

    # Frame para conteúdo dentro do lado direito
    frame_conteudo = ctk.CTkFrame(frame_direito, fg_color='transparent')
    frame_conteudo.pack(fill='both', expand=True)
