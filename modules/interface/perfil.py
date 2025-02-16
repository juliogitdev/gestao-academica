import customtkinter as ctk
from modules.data import json_handler, validators  # Importando o módulo de validadores
from tkinter import messagebox
from modules.interface import dashboard, login  # Assumindo que você tem um módulo 'login' com a tela de login

def fechar_programa(root):
    root.quit()  # Encerra qualquer execução que esteja pendente
    root.destroy()  # Fecha a janela do Tkinter corretamente

def tela_perfil(root, matricula):
    # Limpa a tela
    for widget in root.winfo_children():
        widget.destroy()

    # Cores principais
    cor_principal = "#2e8b57"  # Verde
    cor_secundaria = "#4682b4"

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

    # Frame principal
    frame_principal = ctk.CTkFrame(root, corner_radius=10)
    frame_principal.place(relx=0.5, rely=0.5, relwidth=0.85, relheight=0.85, anchor='center')

    # Título
    label_titulo = ctk.CTkLabel(
        frame_principal, text=f"Perfil de {aluno['nome']}", 
        font=("Arial", 22, "bold"), text_color=cor_principal
    )
    label_titulo.pack(pady=15)

    # Função para salvar as alterações
    def salvar_alteracoes():
        novo_nome = entry_nome.get()
        novo_email = entry_email.get()

        # Validações
        valido_nome, erro_nome = validators.validar_nome(novo_nome)
        valido_email, erro_email = validators.validar_email(novo_email)

        if not valido_nome:
            messagebox.showerror("Erro", erro_nome['error'])
            return

        if not valido_email:
            messagebox.showerror("Erro", erro_email['error'])
            return

        if novo_nome != aluno['nome']:
            aluno['nome'] = novo_nome
        if novo_email != aluno['email']:
            aluno['email'] = novo_email

        try:
            json_handler.salvar_dados(dados)  # Supondo que você tenha uma função para salvar os dados
            messagebox.showinfo("Sucesso", "Dados atualizados com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar os dados: {e}")

    # Dados do aluno
    label_nome = ctk.CTkLabel(frame_principal, text="Nome:", font=("Arial", 14))
    label_nome.pack(pady=5)

    entry_nome = ctk.CTkEntry(frame_principal, font=("Arial", 14))
    entry_nome.insert(0, aluno['nome'])
    entry_nome.pack(pady=5)

    label_email = ctk.CTkLabel(frame_principal, text="E-mail:", font=("Arial", 14))
    label_email.pack(pady=5)

    entry_email = ctk.CTkEntry(frame_principal, font=("Arial", 14))
    entry_email.insert(0, aluno['email'])
    entry_email.pack(pady=5)

    # Botão para salvar alterações
    button_salvar = ctk.CTkButton(
        frame_principal, text="Salvar Alterações", 
        font=("Arial", 18, "bold"),
         hover_color=cor_principal,
        command=salvar_alteracoes
    )
    button_salvar.pack(pady=15)

    # Botão de Voltar
    button_voltar = ctk.CTkButton(
        root, text="Voltar", 
        font=("Arial", 18, "bold"),
         hover_color=cor_principal,
        command=lambda: dashboard.exibir_dashboard(root, matricula)
    )
    button_voltar.place(relx=0.15, rely=0.96, anchor='center')

    # Botão de Logout
    button_logout = ctk.CTkButton(
        frame_principal, text="Logout", 
        font=("Arial", 18, "bold"),
        hover_color='red',
         fg_color=cor_principal,
        command=lambda: login.tela_login(root)  # Supondo que você tenha uma função para exibir a tela de login
    )
    button_logout.place(relx=0.87, rely=0.96, anchor='center')

    # Ao fechar, chamamos a função de limpar na janela principal
    root.protocol("WM_DELETE_WINDOW", lambda: fechar_programa(root))
