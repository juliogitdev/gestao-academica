import customtkinter as ctk
from modules.data import json_handler, validators  # Importando o módulo de validadores
from tkinter import messagebox
from modules.interface import dashboard, login
import config

def fechar_programa(root):
    # Encerra qualquer execução que esteja pendente e fecha a janela do Tkinter
    root.quit()  # Finaliza a execução pendente do programa
    root.destroy()  # Fecha a janela do Tkinter corretamente

def trocar_tema(root, matricula):
    # Altera entre os temas claro e escuro
    if config.TEMA == 'light':
        config.TEMA = 'dark'  # Se estiver no tema claro, muda para o escuro
    else:
        config.TEMA = 'light'  # Se estiver no tema escuro, muda para o claro
    
    ctk.set_appearance_mode(config.TEMA)  # Aplica o novo tema
    return tela_perfil(root, matricula)  # Exibe a tela de perfil novamente após a mudança de tema

def tela_perfil(root, matricula):
    # Limpa a tela para desenhar a tela de perfil do aluno
    for widget in root.winfo_children():
        widget.destroy()

    # Definindo as cores principais e secundárias para a interface
    cor_principal = "#2e8b57"  # Verde
    cor_secundaria = "#4682b4"  # Azul

    # Carregar os dados do aluno a partir do arquivo JSON
    try:
        dados = json_handler.carregar_dados()  # Carrega os dados de alunos
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao carregar os dados: {e}")  # Exibe um erro caso falhe
        return

    aluno = dados['alunos'].get(matricula)  # Recupera os dados do aluno com base na matrícula
    if not aluno:
        messagebox.showerror("Erro", "Aluno não encontrado.")  # Caso o aluno não exista, exibe erro
        return

    # Criação do frame principal que contém os elementos da tela de perfil
    frame_principal = ctk.CTkFrame(root, corner_radius=10)
    frame_principal.place(relx=0.5, rely=0.5, relwidth=0.85, relheight=0.85, anchor='center')

    # Título da tela, exibindo o nome do aluno
    label_titulo = ctk.CTkLabel(
        frame_principal, text=f"Perfil de {aluno['nome']}", 
        font=("Arial", 22, "bold"), text_color=cor_principal
    )
    label_titulo.pack(pady=15)

    # Função que salva as alterações feitas pelo usuário no perfil
    def salvar_alteracoes():
        novo_nome = entry_nome.get()  # Captura o novo nome inserido
        novo_email = entry_email.get()  # Captura o novo email inserido

        # Valida os dados inseridos
        valido_nome, erro_nome = validators.validar_nome(novo_nome)
        valido_email, erro_email = validators.validar_email(novo_email)

        if not valido_nome:
            messagebox.showerror("Erro", erro_nome['error'])  # Exibe erro se o nome não for válido
            return

        if not valido_email:
            messagebox.showerror("Erro", erro_email['error'])  # Exibe erro se o email não for válido
            return

        # Atualiza os dados do aluno se houver mudanças
        if novo_nome != aluno['nome']:
            aluno['nome'] = novo_nome
        if novo_email != aluno['email']:
            aluno['email'] = novo_email

        try:
            json_handler.salvar_dados(dados)  # Tenta salvar os dados modificados
            messagebox.showinfo("Sucesso", "Dados atualizados com sucesso!")  # Exibe mensagem de sucesso
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar os dados: {e}")  # Exibe mensagem de erro caso falhe

    # Campo para edição do nome
    label_nome = ctk.CTkLabel(frame_principal, text="Nome:", font=("Arial", 14))
    label_nome.pack(pady=5)

    entry_nome = ctk.CTkEntry(frame_principal, font=("Arial", 14))
    entry_nome.insert(0, aluno['nome'])  # Insere o nome atual do aluno
    entry_nome.pack(pady=5)

    # Campo para edição do e-mail
    label_email = ctk.CTkLabel(frame_principal, text="E-mail:", font=("Arial", 14))
    label_email.pack(pady=5)

    entry_email = ctk.CTkEntry(frame_principal, font=("Arial", 14))
    entry_email.insert(0, aluno['email'])  # Insere o e-mail atual do aluno
    entry_email.pack(pady=5)

    # Botão para salvar as alterações
    button_salvar = ctk.CTkButton(
        frame_principal, text="Salvar Alterações", 
        font=("Arial", 18, "bold"),
         hover_color=cor_principal,
        command=salvar_alteracoes  # Chama a função de salvar alterações
    )

    # Botão para voltar à tela anterior (dashboard)
    button_voltar = ctk.CTkButton(
        root, text="Voltar", 
        font=("Arial", 18, "bold"),
         hover_color=cor_principal,
        command=lambda: dashboard.exibir_dashboard(root, matricula)  # Volta para o dashboard do aluno
    )
    button_voltar.place(relx=0.15, rely=0.96, anchor='center')

    # Botão de logout que leva à tela de login
    button_logout = ctk.CTkButton(
        frame_principal, text="Logout", 
        font=("Arial", 18, "bold"),
        hover_color='red',
         fg_color=cor_principal,
        command=lambda: login.tela_login(root)  # Chama a função para exibir a tela de login
    )
    button_logout.place(relx=0.87, rely=0.96, anchor='center')

    # Botão para trocar entre os temas
    button_tema = ctk.CTkButton(frame_principal, text='Trocar tema', font=("Arial", 18, "bold"),
         hover_color=cor_principal, command= lambda: trocar_tema(root, matricula))  # Troca entre os temas
    button_tema.pack(pady=20)
    button_salvar.pack(pady=15)

    def excluir_conta(matricula):
        excluir_status = messagebox.askyesno('Excluir conta', 'Tem certeza que deseja excluir sua conta? Todos os seus dados serão apagado.')
        if excluir_status:
            json_handler.remover_aluno(matricula)
            return login.tela_login(root)

    button_excluir_conta = ctk.CTkButton(frame_principal, text="Excluir conta", font=("Arial",  18, "bold"), fg_color='red', command= lambda: excluir_conta(matricula))
    button_excluir_conta.pack(pady=10)
    # Quando a janela for fechada, chama a função para encerrar corretamente o programa
    root.protocol("WM_DELETE_WINDOW", lambda: fechar_programa(root))
