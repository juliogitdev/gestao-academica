import customtkinter as ctk
from modules.data import json_handler, validators
from modules.interface import dashboard
from tkinter import messagebox

# Função para abrir a tela de cadastro de curso
def tela_adicionar_curso(root, matricula):
    janela = ctk.CTkToplevel(root)  # Cria uma nova janela acima da principal
    janela.lift()
    janela.attributes('-topmost', True)
    janela.geometry("600x400")  # Define o tamanho da janela
    janela.title("Cadastrar curso")  # Título da janela

    frame_itens = ctk.CTkFrame(janela)  # Cria o frame onde ficam os itens do formulário
    frame_itens.place(relx=0.5, rely=0.5, anchor='center')  # Centraliza o frame

    # Campo de entrada para o nome do curso
    input_curso = ctk.CTkEntry(frame_itens, width=200, height=40, placeholder_text="Nome do curso")
    input_curso.pack(pady=20, padx=50)

    # Função para fechar a janela e adicionar o curso, se o nome for válido
    def fechar_janela():
        curso_nome = input_curso.get()  # Obtém o nome do curso digitado

        if validators.validar_nome(curso_nome)[0]:  # Valida o nome do curso
            json_handler.adicionar_curso(curso_nome, matricula)  # Adiciona o curso no sistema
            janela.destroy()  # Fecha a janela de cadastro
            return tela_cursos(root, matricula)  # Atualiza a tela de cursos cadastrados
        
        return messagebox.showerror('Dados Inválido', "Digite um nome inválido")  # Exibe erro se o nome for inválido

    # Botão para cadastrar o curso
    botao_enviar = ctk.CTkButton(frame_itens, width=150, height=40, text="Cadastrar", command=fechar_janela)
    botao_enviar.pack(pady=10)

# Função para mostrar os detalhes do curso
def mostrar_detalhes(root, matricula, id_curso):
    janela = ctk.CTkToplevel(root)
    janela.geometry("600x400")
    janela.title("Detalhes do curso")
    janela.lift()
    janela.attributes('-topmost', True)
    janela.resizable(False, False)  # Impede o redimensionamento da janela

    dados = json_handler.carregar_dados()  # Carrega os dados do sistema
    dados_curso = dados['cursos'][id_curso]  # Pega os dados do curso específico

    disciplinas_id = dados_curso['id_disciplinas']  # Pega as disciplinas do curso

    # Exibe o nome do curso e a quantidade de disciplinas
    label_nome_curso = ctk.CTkLabel(janela, text=f'Nome do curso: {dados_curso["nome"]}', font=("Arial", 18))
    label_qtd_disciplinas = ctk.CTkLabel(janela, text=f'Quantidade de disciplinas do curso: {len(disciplinas_id)}', font=("Arial", 18))
    label_nome_curso.pack(pady=10, padx=10)
    label_qtd_disciplinas.pack(pady=10, padx=10)

    # Exibe o título "Disciplinas"
    ctk.CTkLabel(janela, text='Disciplinas: ', font=("Arial", 22, 'bold')).pack(anchor='w', padx=40)

    frame_disciplinas = ctk.CTkScrollableFrame(janela)  # Cria uma área rolável para as disciplinas
    frame_disciplinas.pack(padx=20, fill='x', expand=True)

    # Exibe as disciplinas, caso existam
    if len(disciplinas_id) > 0:
        for id in disciplinas_id:
            disciplina_nome = dados['disciplinas'][id]['nome']
            ctk.CTkLabel(frame_disciplinas, text=disciplina_nome, font=("Arial", 18)).pack(anchor='w', padx=10, pady=5)
    else:
        ctk.CTkLabel(frame_disciplinas, text='Nenhuma disciplina cadastrada nesse curso', font=("Arial", 18)).pack(pady=10)

# Função para excluir um curso
def excluir_curso(id_curso, root, matricula):
    resposta = messagebox.askyesno('Excluir curso', 'Tem certeza que deseja remover esse curso?\nCaso remova, todas as disciplinas e notas relacionadas ao curso serão removidas!')

    if resposta:  # Se o usuário confirmar, exclui o curso
        json_handler.remover_curso(id_curso)

    tela_cursos(root, matricula)  # Atualiza a tela de cursos cadastrados

# Função para exibir os cursos cadastrados
def tela_cursos(root, matricula):
    for widget in root.winfo_children():  # Remove todos os widgets da tela anterior
        widget.destroy()

    cor_verde = ctk.ThemeManager.theme["CTkButton"]["fg_color"]
    cor_vermelho = "#bd0003"  # Cor vermelha para o botão de excluir

    # Cria o frame que vai conter os cursos cadastrados
    frame_cursos_cadastrados = ctk.CTkFrame(root)
    frame_cursos_cadastrados.place(relx=0.05, rely=0.1, relwidth=0.9, relheight=0.8)

    # Botão de voltar para a tela principal
    button_voltar = ctk.CTkButton(root, text="Voltar", font=("Arial", 18, "bold"), border_color=cor_verde, border_width=1, command= lambda: dashboard.exibir_dashboard(root, matricula))
    button_voltar.place(relx=0.05, rely=0.92)

    # Título da lista de cursos cadastrados
    label_cursos_cadastrados = ctk.CTkLabel(frame_cursos_cadastrados, font=("Arial", 25, "bold"), text="Cursos cadastrados:")
    label_cursos_cadastrados.place(relx=0.05, rely=0.05)

    # Botão para cadastrar um novo curso
    button_cadastrar_curso = ctk.CTkButton(frame_cursos_cadastrados, text="Cadastrar curso", font=("Arial", 18), command= lambda: tela_adicionar_curso(root, matricula))
    button_cadastrar_curso.place(relx= 0.7, rely=0.05)

    # Cria o frame rolável onde os cursos serão listados
    frame_tabela = ctk.CTkScrollableFrame(frame_cursos_cadastrados)
    frame_tabela.place(relx=0.05, rely= 0.15, relwidth=0.9, relheight=0.8)

    dados = json_handler.carregar_dados()  # Carrega os dados do sistema
    cursos_id = dados['alunos'][matricula]['cursos']  # Pega os cursos do aluno
    cursos = []

    # Adiciona os cursos na lista
    for id in cursos_id:
        cursos.append(dados['cursos'][id])

    # Exibe os cursos cadastrados
    for i, curso in enumerate(cursos):
        frame_curso = ctk.CTkFrame(frame_tabela, corner_radius=5)
        frame_curso.pack(pady=3, fill='x', padx=5)

        label = ctk.CTkLabel(frame_curso, font=("Arial", 18, 'bold'), text=curso["nome"], height=30)
        label.pack(anchor='w', padx=5)

        # Botão para ver os detalhes do curso
        botao_detalhes = ctk.CTkButton(frame_curso, text="Detalhes", font=('Arial', 13, 'bold'), command= lambda id_curso = cursos_id[i]: mostrar_detalhes(root, matricula, id_curso))
        botao_detalhes.place(relx=0.72, relwidth=0.15, rely=0.5, anchor='center')

        # Botão para excluir o curso
        botao_excluir = ctk.CTkButton(frame_curso, text="Excluir", font=('Arial', 14, 'bold'), fg_color=cor_vermelho, hover_color=cor_vermelho, border_width=1, border_color=cor_vermelho, 
                                      command=lambda id_curso = cursos_id[i] : excluir_curso(id_curso, root, matricula))

        botao_excluir.place(relx=0.9, relwidth=0.15, rely=0.5, anchor='center')
