import customtkinter as ctk
from modules.data import json_handler, validators
from modules.interface import dashboard
from tkinter import messagebox


def tela_cadastrar_curso(root, matricula):
    for widget in root.winfo_children():
        widget.destroy()

    cor_verde = ctk.ThemeManager.theme["CTkButton"]["fg_color"]

    frame_cursos_cadastrados = ctk.CTkFrame(root)
    frame_cursos_cadastrados.place(relx=0.05, rely=0.1, relwidth=0.9, relheight=0.8)

    button_voltar = ctk.CTkButton(root, text="Voltar", fg_color='transparent', font=("Arial", 18, "bold"), border_color=cor_verde, border_width=1, command= lambda: dashboard.exibir_dashboard(root, matricula, True))
    button_voltar.place(relx=0.05, rely=0.92)

    label_cursos_cadastrados = ctk.CTkLabel(frame_cursos_cadastrados, font=("Arial", 20, "bold"), text="Cursos cadastrados:")
    label_cursos_cadastrados.place(relx=0.05, rely=0.05)

    button_cadastrar_curso = ctk.CTkButton(frame_cursos_cadastrados, text="Cadastrar curso", font=("Arial", 18))
    button_cadastrar_curso.place(relx= 0.7, rely=0.05)

    frame_tabela = ctk.CTkScrollableFrame(frame_cursos_cadastrados)
    frame_tabela.place(relx=0.05, rely= 0.15, relwidth=0.9, relheight=0.8)

    dados = json_handler.carregar_dados()
    cursos_id = dados['alunos'][matricula]['cursos']
    cursos = []

    for id in cursos_id:
        cursos.append(dados['cursos'][id])
    


    for i, curso in enumerate(cursos, start=1):  # Começa na linha 1 (segunda linha)
        label = ctk.CTkLabel(frame_tabela, font=("Arial", 18, 'bold'), text=curso["nome"], corner_radius=5)
        label.pack(pady=3)