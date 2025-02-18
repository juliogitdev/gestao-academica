import customtkinter as ctk
from tkinter import messagebox
from modules.data import json_handler, validators
from modules.interface import dashboard, cadastro_aluno

# Função que realiza o login do aluno
def logar_aluno(input_matricula, input_email, root):
    matricula = input_matricula.get()  # Obtém o número de matrícula inserido
    email = input_email.get()  # Obtém o email inserido

    # Valida a matrícula e o email utilizando funções específicas
    if validators.validar_email(email) and validators.validar_matricula(matricula):
        # Verifica se a combinação de matrícula e email está correta
        autorizaçao_login, error = json_handler.verificar_login(matricula, email)
        
        # Se a autenticação falhar, exibe um erro
        if not autorizaçao_login:
            return messagebox.showerror(error[0], "Dados inválidos")
        
        # Caso contrário, exibe o dashboard do aluno
        return dashboard.exibir_dashboard(root, matricula)

    # Se os dados não forem válidos, exibe um erro
    return messagebox.showerror(error[0], "Dados inválidos")


# Função que exibe a tela de login
def tela_login(root):

    # Limpa a tela atual antes de exibir a tela de login
    for widget in root.winfo_children():
        widget.destroy()

    # Criação do frame principal da tela de login
    tela_login = ctk.CTkFrame(root)
    tela_login.pack(fill="both", expand=True)

    # Frame para agrupar os itens da tela
    frame_itens = ctk.CTkFrame(tela_login)
    frame_itens.place(relx = 0.5, rely=0.5, anchor="center")

    # Título da tela de login
    label_login = ctk.CTkLabel(frame_itens, text="Login", font=("Arial", 16, "bold"))
    label_login.pack(pady=10)

    # Campo de entrada para matrícula
    input_matricula = ctk.CTkEntry(frame_itens, width=200, height=40, placeholder_text="Matricula")
    input_matricula.pack(pady=3, padx = 10)

    # Campo de entrada para email
    input_email = ctk.CTkEntry(frame_itens, width=200, height=40, placeholder_text="Email")
    input_email.pack(pady=3, padx = 10)

    # Botão para enviar os dados de login
    botao_enviar = ctk.CTkButton(frame_itens, width=150, height=40, text="Entrar", command=lambda: logar_aluno(input_matricula, input_email, root))
    botao_enviar.pack(pady=20)

    # Botão para criar uma nova conta
    botao_cadastrar = ctk.CTkButton(frame_itens, width=80, height=20, fg_color='transparent',text="Criar conta", command=lambda: cadastro_aluno.tela_cadastro_aluno(root))
    botao_cadastrar.pack(padx = 50, pady = 10)
