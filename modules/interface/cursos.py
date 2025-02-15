import customtkinter as ctk
from modules.data import json_handler, validators
from modules.interface import dashboard
from tkinter import messagebox

def tela_adicionar_curso(root, matricula):
    janela = ctk.CTkToplevel(root)
    janela.geometry("600x400")
    janela.title("Cadastrar curso")

    # Garante que a janela fique acima da principal
    janela.lift()
    janela.attributes('-topmost', True)

    frame_itens = ctk.CTkFrame(janela)
    frame_itens.place(relx=0.5, rely=0.5, anchor='center')

    input_curso = ctk.CTkEntry(frame_itens, width=200, height=40, placeholder_text="Nome do curso")
    input_curso.pack(pady=20, padx=50)

    def fechar_janela():
        curso_nome= input_curso.get()

        if validators.validar_nome(curso_nome)[0]:
            json_handler.adicionar_curso(curso_nome, matricula)
            janela.destroy()
            return tela_cursos(root, matricula)
        
        return messagebox.showerror('Dados Inválido', "Digite um nome inválido")

        


    botao_enviar = ctk.CTkButton(frame_itens, width=150, height=40, text="Cadastrar", command=fechar_janela)
    botao_enviar.pack(pady=10)

def mostrar_detalhes(root, matricula, id_curso):
    janela = ctk.CTkToplevel(root)
    janela.geometry("600x400")
    janela.title("Detalhes do curso")
    janela.lift()
    janela.attributes('-topmost', True)
    janela.resizable(False, False)


    dados = json_handler.carregar_dados()
    dados_curso = dados['cursos'][id_curso]

    disciplinas_id = dados_curso['id_disciplinas']

    label_nome_curso = ctk.CTkLabel(janela, text=f'Nome do curso: {dados_curso['nome']}', font=("Arial", 18))
    label_qtd_disciplinas = ctk.CTkLabel(janela, text=f'Quantidade de disciplinas do curso: {len(disciplinas_id)}', font=("Arial", 18))
    label_nome_curso.pack(pady=10, padx=10)
    label_qtd_disciplinas.pack(pady=10, padx=10)

    #label disciplinas
    ctk.CTkLabel(janela, text='Cursos: ', font=("Arial", 22, 'bold')).pack(anchor='w', padx=40)

    frame_disciplinas = ctk.CTkScrollableFrame(janela)
    frame_disciplinas.pack(padx=20, fill='x', expand=True)

    if len(disciplinas_id)>0:
        for id in disciplinas_id:
            disciplina_nome = dados['disciplinas'][id]['nome']
            ctk.CTkLabel(frame_disciplinas, text=disciplina_nome, font=("Arial", 18)).pack(anchor='w', padx=10, pady=5)
    else:
        ctk.CTkLabel(frame_disciplinas, text='Nenhuma disciplina cadastrado nesse curso', font=("Arial", 18)).pack(pady=10)
                

    

def excluir_curso(id_curso, root, matricula):
    resposta = messagebox.askyesno('Excluir curso', 'Tem certeza que deseja remover esse curso?\ncaso remova, todas as disciplinas e notas relacionadas ao curso será removido!')
    

    if resposta:
        json_handler.remover_curso(id_curso)

    tela_cursos(root, matricula)
    

def tela_cursos(root, matricula):
    for widget in root.winfo_children():
        widget.destroy()

    cor_verde = ctk.ThemeManager.theme["CTkButton"]["fg_color"]
    cor_vermelho = "#bd0003"

    frame_cursos_cadastrados = ctk.CTkFrame(root)
    frame_cursos_cadastrados.place(relx=0.05, rely=0.1, relwidth=0.9, relheight=0.8)

    button_voltar = ctk.CTkButton(root, text="Voltar", fg_color='transparent', font=("Arial", 18, "bold"), border_color=cor_verde, border_width=1, command= lambda: dashboard.exibir_dashboard(root, matricula, True))
    button_voltar.place(relx=0.05, rely=0.92)

    label_cursos_cadastrados = ctk.CTkLabel(frame_cursos_cadastrados, font=("Arial", 25, "bold"), text="Cursos cadastrados:")
    label_cursos_cadastrados.place(relx=0.05, rely=0.05)

    button_cadastrar_curso = ctk.CTkButton(frame_cursos_cadastrados, text="Cadastrar curso", font=("Arial", 18), command= lambda: tela_adicionar_curso(root, matricula))
    button_cadastrar_curso.place(relx= 0.7, rely=0.05)

    frame_tabela = ctk.CTkScrollableFrame(frame_cursos_cadastrados)
    frame_tabela.place(relx=0.05, rely= 0.15, relwidth=0.9, relheight=0.8)

    dados = json_handler.carregar_dados()
    cursos_id = dados['alunos'][matricula]['cursos']
    cursos = []

    for id in cursos_id:
        cursos.append(dados['cursos'][id])
    


    for i, curso in enumerate(cursos):
        frame_curso = ctk.CTkFrame(frame_tabela, fg_color="gray20", corner_radius=5)
        frame_curso.pack(pady=3, fill='x', padx=5)

        label = ctk.CTkLabel(frame_curso, font=("Arial", 18, 'bold'), text=curso["nome"])
        label.pack(anchor='w')

        botao_detalhes = ctk.CTkButton(frame_curso, text="Detalhes", font=('Arial', 13, 'bold'), command= lambda id_curso = cursos_id
                                       
                                       [i]: mostrar_detalhes(root, matricula, id_curso))
        botao_detalhes.place(relx=0.6, relwidth=0.15)

        botao_excluir = ctk.CTkButton(frame_curso, text="Excluir", font=('Arial', 14, 'bold'), fg_color='transparent', hover_color=cor_vermelho, border_width=1, border_color=cor_vermelho, 
                                      command=lambda id_curso = cursos_id[i] : excluir_curso(id_curso, root, matricula))

        
        botao_excluir.place(relx=0.8, relwidth=0.15)