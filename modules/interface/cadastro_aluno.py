import customtkinter as ctk
from tkinter import messagebox
from modules.data import validators, json_handler
from modules.interface import dashboard, login

# Função responsável por cadastrar o aluno
def cadastrar_aluno(input_matricula, input_nome, input_email, root):
    # Obtém os valores digitados nos campos
    matricula = input_matricula.get()
    nome = input_nome.get()
    email = input_email.get()

    # Valida os dados do aluno
    matricula_status = validators.validar_matricula(matricula)[0]
    nome_status = validators.validar_nome(nome)[0]
    email_status = validators.validar_email(email)[0]

    # Verifica se todos os dados estão válidos
    if matricula_status and nome_status and email_status:
        # Tenta cadastrar o aluno no arquivo JSON
        cadastro_status = json_handler.adicionar_aluno(nome, matricula, email)
        if cadastro_status:
            # Se o cadastro for bem-sucedido, exibe uma mensagem de sucesso
            messagebox.showinfo('Sucesso', 'Aluno cadastrado com sucesso')
            return dashboard.exibir_dashboard(root, matricula)  # Exibe o painel do aluno
        else:
            # Caso a matrícula já exista, exibe uma mensagem de erro
            messagebox.showerror('Matricula existente', 'Aluno com essa matricula já registrado!')
            return
    else:
        # Se algum dado estiver incorreto, exibe uma mensagem de erro
        messagebox.showerror('error', 'Por favor, preencha os campos corretamente')
        return

# Função que cria a tela de cadastro de aluno
def tela_cadastro_aluno(root):
    # Remove todos os widgets (componentes) da tela anterior
    for widget in root.winfo_children():
        widget.destroy()

    # Cria um novo quadro para a tela de cadastro
    tela_cadastro = ctk.CTkFrame(root)
    tela_cadastro.pack(fill="both", expand=True)

    # Cria um quadro para os itens do formulário
    frame_itens = ctk.CTkFrame(tela_cadastro)
    frame_itens.place(relx = 0.5, rely=0.5, anchor="center")  # Centraliza o formulário

    # Título da tela de cadastro
    label_cadastro_aluno = ctk.CTkLabel(frame_itens, text="Cadastrar Aluno", font=("Arial", 16, "bold"))
    label_cadastro_aluno.pack(pady=10)

    # Campo para inserir a matrícula do aluno
    input_matricula = ctk.CTkEntry(frame_itens, width=200, height=40, placeholder_text="Matricula")
    input_matricula.pack(pady=3, padx = 10)

    # Campo para inserir o nome completo do aluno
    input_nome = ctk.CTkEntry(frame_itens, width=200, height=40, placeholder_text="Nome completo")
    input_nome.pack(pady=3, padx = 10)

    # Campo para inserir o email do aluno
    input_email = ctk.CTkEntry(frame_itens, width=200, height=40, placeholder_text="Email")
    input_email.pack(pady=3, padx = 10)

    # Botão para enviar o formulário e cadastrar o aluno
    botao_enviar = ctk.CTkButton(frame_itens, width=150, height=40, text="Cadastrar", command= lambda: cadastrar_aluno(input_matricula, input_nome, input_email, root))
    botao_enviar.pack(pady=20)

    # Botão para ir para a tela de login, caso o aluno já tenha cadastro
    botao_login = ctk.CTkButton(frame_itens, width=80, height=20, fg_color='transparent',text="Fazer login", command=lambda: login.tela_login(root))
    botao_login.pack(padx = 50, pady = 10)
