import customtkinter as ctk
from modules.data import json_handler
from modules.interface import cursos, disciplinas, notas, graficos_desempenho, perfil

def exibir_dashboard(root, matricula):
    # Limpar widgets existentes
    for widget in root.winfo_children():
        widget.destroy()

    # Carregar dados
    dados = json_handler.carregar_dados()
    dados_aluno = dados['alunos'][matricula]
    nome_aluno = dados_aluno['nome']
    cursos_aluno = dados_aluno['cursos']
    id_disciplinas = dados_aluno['disciplinas']
    
    cor_verde = "#2e8b57"
    cor_alerta = "#FF6347"  # Cor mais suave de alerta

    # Tela principal (dashboard)
    tela_dashboard = ctk.CTkFrame(root)
    tela_dashboard.pack(fill="both", expand=True)

    # Frame para título
    frame_titulo = ctk.CTkFrame(tela_dashboard, corner_radius=0, fg_color=cor_verde)
    frame_titulo.place(relx=0, rely=0, relwidth=1, relheight=0.1)

    # Texto "SISTEMA DE GESTÃO ACADÊMICA"
    label_gestao_academica = ctk.CTkLabel(
        frame_titulo,
        font=('Arial', 28, 'bold'),
        text="SISTEMA DE GESTÃO ACADÊMICA",
        text_color="white"
    )
    label_gestao_academica.place(relx=0.5, rely=0.5, anchor='center')

    # Frame para os botões de navegação (menu)
    frame_nav = ctk.CTkFrame(tela_dashboard, corner_radius=0)
    frame_nav.place(relx=0, rely=0.1, relwidth=1, relheight=0.07)

    # Botões de navegação
    button_cursos = ctk.CTkButton(
        frame_nav,
        text='Cursos',
        font=('Arial', 16, 'bold'),
        fg_color="transparent",
        hover_color=cor_verde,
        command=lambda: cursos.tela_cursos(root, matricula)
    )
    button_cursos.grid(row=0, column=0, sticky="nsew")

    button_disciplinas = ctk.CTkButton(
        frame_nav,
        text='Disciplinas',
        font=('Arial', 16, 'bold'),
        fg_color="transparent",
        hover_color=cor_verde,
        command=lambda: disciplinas.mostrar_disciplinas(root, matricula)
    )
    button_disciplinas.grid(row=0, column=1, sticky="nsew")

    button_notas = ctk.CTkButton(
        frame_nav,
        text='Notas',
        font=('Arial', 16, 'bold'),
        fg_color="transparent",
        hover_color=cor_verde,
        command=lambda: notas.mostrar_notas(root, matricula)
    )
    button_notas.grid(row=0, column=2, sticky="nsew")

    button_desempenho = ctk.CTkButton(
        frame_nav,
        text='Desempenho',
        font=('Arial', 16, 'bold'),
        fg_color="transparent",
        hover_color=cor_verde,
        command=lambda: graficos_desempenho.tela_desempenho(root, frame_conteudo, matricula)
    )
    button_desempenho.grid(row=0, column=3, sticky="nsew")

    button_perfil = ctk.CTkButton(
        frame_nav,
        text='Perfil',
        font=('Arial', 16, 'bold'),
        fg_color="transparent",
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
    frame_conteudo = ctk.CTkFrame(frame_direito)  # Cor neutra
    frame_conteudo.pack(fill='both', expand=True)

    # Saudação ao aluno
    label_saudacao = ctk.CTkLabel(
        frame_conteudo,
        font=('Arial', 32, 'bold'),
        text=f"Olá, {nome_aluno}!",
        text_color=cor_verde
    )
    label_saudacao.pack(pady=20, anchor='w', padx=30)

    # Frame para cursos (scrollable)
    frame_cursos = ctk.CTkScrollableFrame(frame_conteudo)  # Ajuste de altura
    label_cursos = ctk.CTkLabel(
        frame_conteudo,
        font=('Arial', 18, 'bold'),
        text="Cursos matriculados:",
        text_color=cor_verde
    )
    label_cursos.pack(anchor='w', pady=10, padx=30)
    frame_cursos.pack(padx=20, fill='x')

    for i, curso_id in enumerate(cursos_aluno):
        nome_curso = dados['cursos'][curso_id]['nome']
        label_curso = ctk.CTkLabel(
            frame_cursos,
            font=('Arial', 16, 'bold'),
            text=nome_curso,
            anchor="w",
            justify="left"
        )
        label_curso.pack(anchor='w', padx=30, pady=5)

    # Exibir alerta de médias abaixo de 70 e diferente de 0
    alertas_media = []
    for disciplina_id in id_disciplinas:
        notas_disciplina = dados['notas'][matricula].get(disciplina_id, [])
        if len(notas_disciplina) >= 2:  # Considera a média das duas notas
            media = sum(notas_disciplina) / len(notas_disciplina)
            if media > 0 and media < 70:
                disciplina_nome = dados['disciplinas'][disciplina_id]['nome']
                alertas_media.append(f"Média de {disciplina_nome} abaixo de 70!")

    # Exibir alertas diretamente no dashboard
    if alertas_media:
        label_alertas = ctk.CTkLabel(
            frame_conteudo,
            text="Alertas de Desempenho:",
            font=('Arial', 18, 'bold'),
            text_color=cor_alerta
        )
        label_alertas.pack(anchor="w", padx=30, pady=10)

        for alerta in alertas_media:
            label_alerta = ctk.CTkLabel(
                frame_conteudo,
                font=('Arial', 14),
                text=alerta,
                text_color=cor_alerta,
                anchor="w",
                justify="left"
            )
            label_alerta.pack(anchor='w', padx=30, pady=5)

