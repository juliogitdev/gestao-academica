import customtkinter as ctk
from modules.interface import dashboard
from modules.data import json_handler, validators
from tkinter import messagebox

def tela_adicionar_disciplina(root, combobox, cursos, matricula):
    nome_curso = combobox.get()
    if nome_curso == "Selecionar curso":
        return messagebox.showinfo("Alerta", "Selecione um curso primeiro.")
    id_curso_selecionado = cursos[nome_curso]
    janela = ctk.CTkToplevel(root)
    janela.geometry("600x400")
    janela.title("Cadastrar disciplina")

    # Garante que a janela fique acima da principal
    janela.lift()
    janela.attributes('-topmost', True)

    frame_itens = ctk.CTkFrame(janela)
    frame_itens.place(relx=0.5, rely=0.5, anchor='center')

    input_curso = ctk.CTkEntry(frame_itens, width=200, height=40, placeholder_text="Nome da disciplina")
    input_curso.pack(pady=20, padx=50)

    def cadastrar_disciplina():
        disciplina_nome = input_curso.get()

        if validators.validar_nome(disciplina_nome)[0]:
            json_handler.adicionar_disciplina(disciplina_nome, id_curso_selecionado)
            janela.destroy()
            return mostrar_disciplinas(root, matricula, nome_curso)  # Passa o nome do curso para re-exibir as disciplinas
            
        return messagebox.showerror('Dados Inválido', "Digite um nome inválido")

    button_cadastrar = ctk.CTkButton(frame_itens, text="Cadastrar", command=cadastrar_disciplina)
    button_cadastrar.pack(pady=10)

def excluir_disciplina(root, id_disciplina, matricula, curso):
    resposta = messagebox.askyesno('Excluir disciplina', 'Tem certeza que deseja remover essa disciplina?\ncaso remova, todas as notas relacionadas a disciplina será removido!')
    

    if resposta:
        json_handler.remover_disciplina(id_disciplina)

    mostrar_disciplinas(root, matricula, curso)

def mostrar_disciplinas(root, matricula, opcao_curso='Selecionar curso'):
    for widget in root.winfo_children():
        widget.destroy()

    cor_verde = ctk.ThemeManager.theme["CTkButton"]["fg_color"]
    cor_vermelho = "#bd0003"

    frame_disciplinas = ctk.CTkFrame(root)
    frame_disciplinas.pack(fill='both', expand=True)

    dados = json_handler.carregar_dados()
    id_cursos = dados['alunos'][matricula]['cursos']
    cursos = {}

    for id_curso in id_cursos:
        curso = dados['cursos'][id_curso]['nome']
        cursos[curso] = id_curso

    nomes_disciplinas = list(cursos.keys())

    frame_label_disciplinas = ctk.CTkFrame(frame_disciplinas)
    frame_label_disciplinas.pack(fill='x', pady=40, padx=20)

    label_disciplinas = ctk.CTkLabel(frame_label_disciplinas, font=("Arial", 22, "bold"), text='Disciplinas')
    label_disciplinas.pack(pady=10)

    frame_scroll_disciplinas = ctk.CTkScrollableFrame(frame_disciplinas)

    def filtrar_disciplinas(curso):
        if curso not in cursos:
            return
        id_curso_selecionado = cursos[curso]
        disciplinas_cursos = dados['cursos'][id_curso_selecionado]["id_disciplinas"]
        for widget in frame_scroll_disciplinas.winfo_children():
            widget.destroy()
        for disciplina_id in disciplinas_cursos:
            disciplina_nome = dados['disciplinas'][disciplina_id]['nome']
            ctk.CTkLabel(frame_scroll_disciplinas, text=disciplina_nome, font=('Arial', 20)).pack(anchor='w', padx=10, pady=5)
            ctk.CTkButton(frame_scroll_disciplinas, text="Excluir", width=50, fg_color=cor_vermelho, font=("Arial",10,"bold"), hover_color='red', command= lambda: excluir_disciplina(root, disciplina_id, matricula, dados['cursos'][id_curso_selecionado]['nome'])).pack(anchor='w', padx=10)

    # Criação da combobox para selecionar o curso e filtrar disciplinas
    combobox = ctk.CTkComboBox(frame_disciplinas, values=nomes_disciplinas, command=filtrar_disciplinas, state='readonly')
    combobox.pack(anchor='w', padx=20, pady=5)

    combobox.set(opcao_curso)
    if opcao_curso != "Selecionar curso":
        filtrar_disciplinas(opcao_curso)  # Aplica diretamente o filtro ao carregar a tela

    frame_scroll_disciplinas.pack(padx=20, fill='both', expand=True)

    frame_buttons = ctk.CTkFrame(root)
    frame_buttons.pack(pady=20, padx=20, fill='x')

    button_adicionar_disciplina = ctk.CTkButton(frame_buttons, text="Adicionar", font=("Arial", 18, "bold"),
                                                command=lambda: tela_adicionar_disciplina(root, combobox, cursos, matricula))
    button_adicionar_disciplina.pack()

    button_voltar = ctk.CTkButton(frame_buttons, text="Voltar", fg_color='transparent', font=("Arial", 18, "bold"),
                                  border_color=cor_verde, border_width=1,
                                  command=lambda: dashboard.exibir_dashboard(root, matricula, True))
    button_voltar.pack(pady=10, anchor='w')

