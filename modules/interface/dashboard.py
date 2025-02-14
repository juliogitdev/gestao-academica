import customtkinter as ctk
from modules.data import json_handler
from modules.interface import cadastro_disciplina, registro_notas, historico_academico, graficos_desempenho, cadastro_curso

def exibir_dashboard(root, matricula, tem_menu = False):
    for widget in root.winfo_children():
        widget.destroy()
    
    dados = json_handler.carregar_dados()
    dados_aluno = dados['alunos'][matricula]

    cor_verde = "#2e8b57"
    
    #tela toda
    tela_dashboard = ctk.CTkFrame(root)
    tela_dashboard.pack(fill="both", expand=True)

    if not tem_menu:
        #frame onde vai ficar sistema de gestao academica
        frame_titulo = ctk.CTkFrame(tela_dashboard, corner_radius=0)
        frame_titulo.place(relx=0, rely=0, relwidth=1, relheight=0.1)

        #texto gestao academica
        label_gestao_academica = ctk.CTkLabel(frame_titulo, font=('Arial', 30, 'bold'), text="SISTEMA DE GESTÃO ACADÊMICA", text_color=cor_verde)
        label_gestao_academica.pack(pady=10)

        #frame esquerdo onde vai ficar o menu
        frame_menu = ctk.CTkFrame(tela_dashboard, border_width=0, corner_radius=0)
        frame_menu.place(relwidth = 0.2, relheight=0.9, relx = 0, rely=0.1)

        #frame onde vai ficar os botoes do menu
        frame_buttons = ctk.CTkFrame(frame_menu)
        frame_buttons.place(relx = 0.5, rely = 0.5, relwidth=0.9, relheight=0.5, anchor='center')

        #botoes do menu
        button_cursos = ctk.CTkButton(frame_buttons , text='cursos', font=('Arial', 15, 'bold'), command= lambda: cadastro_curso.tela_cadastrar_curso(frame_conteudo, matricula))
        button_cursos.pack(fill="both", expand=True, pady=2)

        button_disciplinas = ctk.CTkButton(frame_buttons, text='disciplinas', font=('Arial', 15, 'bold'), command= lambda: cadastro_curso.tela_cadastrar_curso(frame_conteudo, matricula))
        button_disciplinas.pack(fill="both", expand=True, pady=2)

        button_notas = ctk.CTkButton(frame_buttons, text='notas', font=('Arial', 15, 'bold'), command= lambda: cadastro_curso.tela_cadastrar_curso(frame_conteudo, matricula))
        button_notas.pack(fill="both", expand=True, pady=2)

        button_perfil = ctk.CTkButton(frame_buttons, text='perfil', font=('Arial', 15, 'bold'))
        button_perfil.pack(fill="both", expand=True, pady=2)

        button_configuracoes = ctk.CTkButton(frame_buttons, text='configurações', font=('Arial', 15, 'bold'))
        button_configuracoes.pack(fill="both", expand=True, pady=2)

    #frame direito onde vai ficar o conteudo
    frame_direito = ctk.CTkFrame(tela_dashboard)
    frame_direito.place(relwidth = 0.8, relheight=0.9, relx = 0.2, rely=0.1)

    frame_conteudo = ctk.CTkFrame(frame_direito)
    frame_conteudo.pack(fill='both', expand=True)

    
