import customtkinter as ctk  # Importa a biblioteca para criar interfaces gráficas
import tkinter.messagebox as mb  # Importa a biblioteca para mostrar caixas de mensagem
from modules.data import json_handler, validators  # Importa funções para lidar com os dados e validações
from modules.interface import dashboard  # Importa a tela de dashboard

# Função que vai salvar as notas do aluno
def salvar_nota(root, matricula, id_curso, id_disciplina, entrada_nota1, entrada_nota2):
    # Tenta converter o que foi colocado nas caixas de texto para números (notas)
    try:
        nota1_valor = float(entrada_nota1.get())  # Tenta converter Nota 1
        nota2_valor = float(entrada_nota2.get())  # Tenta converter Nota 2
    except ValueError:
        mb.showerror("Erro", "Insira valores numéricos para as notas.")  # Se não for número, mostra erro
        return

    # Valida as notas usando uma função que checa se as notas são válidas
    valido1, erro1 = validators.validar_nota(nota1_valor)
    valido2, erro2 = validators.validar_nota(nota2_valor)
    
    if not valido1 or not valido2:  # Se uma das notas for inválida
        error_message = ""
        if not valido1:
            error_message += f"Nota inválida.\n"
        if not valido2:
            error_message += f"Nota inválida.\n"
        mb.showerror("Erro de Validação", error_message)  # Mostra a mensagem de erro
        return

    # Se as notas forem válidas, prossegue com o salvamento
    dados = json_handler.carregar_dados()  # Carrega os dados do arquivo
    notas = dados['notas']  # Pega as notas dos alunos
    
    # Atualiza as notas no arquivo com os novos valores inseridos
    notas[matricula][id_disciplina][0] = nota1_valor
    notas[matricula][id_disciplina][1] = nota2_valor
    
    json_handler.salvar_dados(dados)  # Salva os dados atualizados no arquivo
    mostrar_notas(root, matricula)  # Chama a função para mostrar as notas atualizadas

# Função que vai exibir as notas na tela
def mostrar_notas(root, matricula):
    # Limpa a tela atual
    for widget in root.winfo_children():
        widget.destroy()
    
    dados = json_handler.carregar_dados()  # Carrega os dados do arquivo
    aluno = dados['alunos'][matricula]  # Pega as informações do aluno
    cursos = aluno['cursos']  # Pega os cursos que o aluno está matriculado
    
    # Cria o frame principal onde as notas serão exibidas
    frame_notas = ctk.CTkFrame(root)
    frame_notas.place(relx=0.5, rely=0.5, relwidth=0.8, relheight=0.8, anchor='center')
    
    # Configura o grid para os widgets ficarem organizados na tela
    frame_notas.grid_rowconfigure(0, weight=0)  # Título
    frame_notas.grid_rowconfigure(1, weight=1)  # Frame rolável para as notas
    frame_notas.grid_rowconfigure(2, weight=0)  # Botão Voltar
    for col in range(7):
        frame_notas.grid_columnconfigure(col, weight=1)

    # Título que vai ser exibido na parte de cima
    label_titulo = ctk.CTkLabel(
        frame_notas, 
        text="Notas do Aluno", 
        font=("Arial", 20, "bold")
    )
    label_titulo.grid(row=0, column=0, columnspan=7, pady=10, padx=10, sticky="ew")
    
    # Frame rolável onde vão ficar as notas organizadas em forma de tabela
    scroll_frame = ctk.CTkScrollableFrame(frame_notas)
    scroll_frame.grid(row=1, column=0, columnspan=7, sticky="nsew", padx=10, pady=10)

    # Organiza as colunas dentro do scroll_frame
    for col in range(7):
        scroll_frame.grid_columnconfigure(col, weight=1)

    row_index = 0
    
    for id_curso in cursos:  # Para cada curso que o aluno está matriculado
        curso = dados['cursos'][id_curso]  # Pega as informações do curso
        
        # Exibe o nome do curso
        ctk.CTkLabel(
            scroll_frame, 
            text=f"Curso: {curso['nome']}", 
            font=("Arial", 16, "bold"), 
            corner_radius=5, 
            fg_color="#2B2B2B", 
            text_color="white"
        ).grid(row=row_index, column=1, columnspan=5, pady=10, sticky="ew")
        row_index += 1
        
        headers = ["Disciplina", "Nota 1", "Nota 2", "Média", "Ação"]
        
        # Cabeçalho da tabela
        for col, text in enumerate(headers, start=1):
            ctk.CTkLabel(
                scroll_frame, 
                text=text, 
                font=("Arial", 14, "bold"), 
                fg_color="#444", 
                text_color="white"
            ).grid(row=row_index, column=col, padx=5, pady=5, sticky="ew")
        row_index += 1
        
        for id_disciplina in curso['id_disciplinas']:  # Para cada disciplina do curso
            disciplina = dados['disciplinas'][id_disciplina]  # Pega as informações da disciplina
            # Lê as notas da disciplina; se não existirem, assume [0, 0]
            notas_disciplina = dados['notas'][matricula].get(id_disciplina, [0, 0])
            media = (notas_disciplina[0] + notas_disciplina[1]) / 2  # Calcula a média
            
            # Exibe o nome da disciplina
            ctk.CTkLabel(
                scroll_frame, 
                text=disciplina["nome"], 
                font=("Arial", 12)
            ).grid(row=row_index, column=1, padx=5, pady=5, sticky="ew")
            
            # Caixa de texto para inserir Nota 1
            entrada_nota1 = ctk.CTkEntry(scroll_frame, width=80)
            entrada_nota1.insert(0, str(notas_disciplina[0]))
            entrada_nota1.grid(row=row_index, column=2, padx=5, pady=5)
            
            # Caixa de texto para inserir Nota 2
            entrada_nota2 = ctk.CTkEntry(scroll_frame, width=80)
            entrada_nota2.insert(0, str(notas_disciplina[1]))
            entrada_nota2.grid(row=row_index, column=3, padx=5, pady=5)
            
            # Exibe a média calculada
            ctk.CTkLabel(
                scroll_frame, 
                text=f"{media:.2f}", 
                font=("Arial", 12, "bold"), 
                text_color="green"
            ).grid(row=row_index, column=4, padx=5, pady=5, sticky="ew")
            
            # Botão para salvar as notas
            btn_salvar = ctk.CTkButton(
                scroll_frame, 
                text="Salvar", 
                command=lambda d=id_disciplina, c=id_curso, en1=entrada_nota1, en2=entrada_nota2: salvar_nota(root, matricula, c, d, en1, en2)
            )
            btn_salvar.grid(row=row_index, column=5, padx=5, pady=5)
            row_index += 1
    
    # Botão Voltar para voltar à tela anterior
    button_voltar = ctk.CTkButton(
        frame_notas, 
        text="Voltar", 
        command=lambda: dashboard.exibir_dashboard(root, matricula)
    )
    button_voltar.grid(row=2, column=0, columnspan=7, pady=10)
