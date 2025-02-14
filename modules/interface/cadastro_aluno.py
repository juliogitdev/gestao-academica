import customtkinter as ctk
from tkinter import messagebox
from modules.data import validators
from modules.data import json_handler

def cadastrar_aluno(input_matricula, input_nome, input_email):
    matricula = input_matricula.get()
    nome = input_nome.get()
    email = input_email.get()

    matricula_status = validators.validar_matricula(matricula)
    nome_status = validators.validar_nome(nome)
    email_status = validators.validar_email(email)

    if matricula_status and nome_status and email_status:
        cadastro_status = json_handler.adicionar_aluno(nome, matricula, email)
        if cadastro_status:
            messagebox.showinfo('Sucesso', 'Aluno cadastrado com sucesso')
        else:
            messagebox.showerror('Matricula existente', 'Aluno com essa matricula já registrado!')
    else:
        messagebox.showerror('error', 'Por favor, preencha os campos corretamente')
    
    

def tela_cadastro_aluno(root):
    for widget in root.winfo_children():
        widget.destroy()

    tela_cadastro = ctk.CTkFrame(root)
    tela_cadastro.pack(fill="both", expand=True)

    frame_itens = ctk.CTkFrame(tela_cadastro)
    frame_itens.place(relx = 0.5, rely=0.5, anchor="center")


    label_cadastro_aluno = ctk.CTkLabel(frame_itens, text="Cadastrar Aluno", font=("Arial", 16, "bold"))
    label_cadastro_aluno.pack(pady=10)


    input_matricula = ctk.CTkEntry(frame_itens, width=200, height=40, placeholder_text="Matricula")
    input_matricula.pack(pady=3, padx = 10)

    input_nome = ctk.CTkEntry(frame_itens, width=200, height=40, placeholder_text="Nome completo")
    input_nome.pack(pady=3, padx = 10)

    input_email = ctk.CTkEntry(frame_itens, width=200, height=40, placeholder_text="Email")
    input_email.pack(pady=3, padx = 10)

    botao_enviar = ctk.CTkButton(frame_itens, width=150, height=40, text="Cadastrar", command= lambda: cadastrar_aluno(input_matricula, input_nome, input_email))
    botao_enviar.pack(pady=20)