# Importação das bibliotecas necessárias
import customtkinter as ctk
from modules.interface import dashboard
from modules.data import json_handler, validators
from tkinter import messagebox

# Função para abrir a tela de adicionar disciplina
def tela_adicionar_disciplina(root, combobox, cursos, matricula):
    nome_curso = combobox.get()  # Pega o nome do curso selecionado na combobox
    
    # Se o usuário não tiver selecionado um curso, mostra um aviso
    if nome_curso == "Selecionar curso":
        return messagebox.showinfo("Alerta", "Selecione um curso primeiro.")
    
    # Pega o ID do curso selecionado
    id_curso_selecionado = cursos[nome_curso]
    
    # Criação de uma nova janela para adicionar disciplina
    janela = ctk.CTkToplevel(root)
    janela.geometry("600x400")
    janela.title("Cadastrar disciplina")

    # Deixa a janela de cadastro sempre por cima
    janela.lift()
    janela.attributes('-topmost', True)

    # Frame para os itens da janela (a parte onde colocamos os widgets)
    frame_itens = ctk.CTkFrame(janela)
    frame_itens.place(relx=0.5, rely=0.5, anchor='center')

    # Caixa de texto para o nome da disciplina
    input_curso = ctk.CTkEntry(frame_itens, width=200, height=40, placeholder_text="Nome da disciplina")
    input_curso.pack(pady=20, padx=50)

    # Função para cadastrar a disciplina no arquivo JSON
    def cadastrar_disciplina():
        disciplina_nome = input_curso.get()  # Pega o nome da disciplina digitado

        # Se o nome da disciplina for válido
        if validators.validar_nome(disciplina_nome)[0]:
            json_handler.adicionar_disciplina(disciplina_nome, id_curso_selecionado)
            janela.destroy()  # Fecha a janela de cadastro
            return mostrar_disciplinas(root, matricula, nome_curso)  # Atualiza as disciplinas do curso

        # Se o nome for inválido, mostra uma mensagem de erro
        return messagebox.showerror('Dados Inválido', "Digite um nome inválido")

    # Botão para cadastrar a disciplina
    button_cadastrar = ctk.CTkButton(frame_itens, text="Cadastrar", command=cadastrar_disciplina)
    button_cadastrar.pack(pady=10)

# Função para excluir uma disciplina
def excluir_disciplina(root, id_disciplina, matricula, curso):
    # Pergunta se o usuário tem certeza de que quer excluir a disciplina
    resposta = messagebox.askyesno('Excluir disciplina', 'Tem certeza que deseja remover essa disciplina?\ncaso remova, todas as notas relacionadas a disciplina será removido!')

    # Se a resposta for sim, exclui a disciplina
    if resposta:
        json_handler.remover_disciplina(id_disciplina)

    # Atualiza a lista de disciplinas após a exclusão
    mostrar_disciplinas(root, matricula, curso)

# Função para exibir as disciplinas do aluno
def mostrar_disciplinas(root, matricula, opcao_curso='Selecionar curso'):
    # Limpa todos os widgets da tela
    for widget in root.winfo_children():
        widget.destroy()

    # Cores para botões
    cor_verde = ctk.ThemeManager.theme["CTkButton"]["fg_color"]
    cor_vermelho = "#bd0003"

    # Criação do frame principal onde tudo vai ficar
    frame_disciplinas = ctk.CTkFrame(root)
    frame_disciplinas.pack(fill='both', expand=True)

    # Carrega os dados dos cursos e disciplinas do arquivo JSON
    dados = json_handler.carregar_dados()
    id_cursos = dados['alunos'][matricula]['cursos']
    cursos = {}

    # Preenche o dicionário de cursos com o nome e ID
    for id_curso in id_cursos:
        curso = dados['cursos'][id_curso]['nome']
        cursos[curso] = id_curso

    # Lista de nomes dos cursos
    nomes_disciplinas = list(cursos.keys())

    # Frame para o título das disciplinas
    frame_label_disciplinas = ctk.CTkFrame(frame_disciplinas)
    frame_label_disciplinas.pack(fill='x', pady=40, padx=20)

    # Título das disciplinas
    label_disciplinas = ctk.CTkLabel(frame_label_disciplinas, font=("Arial", 22, "bold"), text='Disciplinas')
    label_disciplinas.pack(pady=10)

    # Frame para exibir as disciplinas com rolagem
    frame_scroll_disciplinas = ctk.CTkScrollableFrame(frame_disciplinas)

    # Função para filtrar as disciplinas de acordo com o curso selecionado
    def filtrar_disciplinas(curso):
        if curso not in cursos:
            return
        id_curso_selecionado = cursos[curso]
        disciplinas_cursos = dados['cursos'][id_curso_selecionado]["id_disciplinas"]
        
        # Limpa as disciplinas exibidas antes de carregar as novas
        for widget in frame_scroll_disciplinas.winfo_children():
            widget.destroy()

        # Se não houver disciplinas, mostra um alerta
        if not disciplinas_cursos:
            messagebox.showinfo("Aviso", "Este curso não possui disciplinas cadastradas.")
            return

        # Exibe as disciplinas cadastradas
        for disciplina_id in disciplinas_cursos:
            disciplina_nome = dados['disciplinas'][disciplina_id]['nome']
            ctk.CTkLabel(frame_scroll_disciplinas, text=disciplina_nome, font=('Arial', 20)).pack(anchor='w', padx=10, pady=5)
            ctk.CTkButton(frame_scroll_disciplinas, text="Excluir", width=50, fg_color=cor_vermelho, font=("Arial",10,"bold"), hover_color='red', command= lambda: excluir_disciplina(root, disciplina_id, matricula, dados['cursos'][id_curso_selecionado]['nome'])).pack(anchor='w', padx=10)

    # Criação da combobox para selecionar o curso e filtrar as disciplinas
    combobox = ctk.CTkComboBox(frame_disciplinas, values=nomes_disciplinas, command=filtrar_disciplinas, state='readonly')
    combobox.pack(anchor='w', padx=20, pady=5)

    # Seleção do curso caso já tenha um previamente
    combobox.set(opcao_curso)
    if opcao_curso != "Selecionar curso":
        filtrar_disciplinas(opcao_curso)  # Aplica diretamente o filtro ao carregar a tela

    frame_scroll_disciplinas.pack(padx=20, fill='both', expand=True)

    # Botão para adicionar uma nova disciplina
    button_adicionar_disciplina = ctk.CTkButton(frame_disciplinas, text="Adicionar", font=("Arial", 18, "bold"),
                                                command=lambda: tela_adicionar_disciplina(root, combobox, cursos, matricula))
    button_adicionar_disciplina.pack(pady=10)

    # Botão para voltar ao dashboard
    button_voltar = ctk.CTkButton(frame_disciplinas, text="Voltar", font=("Arial", 18, "bold"),
                                  border_color=cor_verde, border_width=1,
                                  command=lambda: dashboard.exibir_dashboard(root, matricula))
    button_voltar.pack(anchor='w', padx=20, pady=20)
