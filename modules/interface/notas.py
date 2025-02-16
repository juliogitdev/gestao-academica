import customtkinter as ctk
import tkinter.messagebox as mb
from modules.data import json_handler, validators
from modules.interface import dashboard

def salvar_nota(root, matricula, id_curso, id_disciplina, entrada_nota1, entrada_nota2):
    # Tenta converter as entradas para float
    try:
        nota1_valor = float(entrada_nota1.get())
        nota2_valor = float(entrada_nota2.get())
    except ValueError:
        mb.showerror("Erro", "Insira valores numéricos para as notas.")
        return

    # Valida as notas usando a função do módulo validators
    valido1, erro1 = validators.validar_nota(nota1_valor)
    valido2, erro2 = validators.validar_nota(nota2_valor)
    
    if not valido1 or not valido2:
        error_message = ""
        if not valido1:
            error_message += f"Nota inválida.\n"
        if not valido2:
            error_message += f"Nota inválida.\n"
        mb.showerror("Erro de Validação", error_message)
        return

    # Se as notas forem válidas, prossegue com o salvamento
    dados = json_handler.carregar_dados()
    notas = dados['notas']
    
    # Atualiza os valores das notas (ajuste conforme sua estrutura de dados)
    notas[matricula][id_disciplina][0] = nota1_valor
    notas[matricula][id_disciplina][1] = nota2_valor
    
    json_handler.salvar_dados(dados)
    mostrar_notas(root, matricula)

def mostrar_notas(root, matricula):
    # Limpa a tela
    for widget in root.winfo_children():
        widget.destroy()
    
    dados = json_handler.carregar_dados()
    aluno = dados['alunos'][matricula]
    cursos = aluno['cursos']
    
    # Frame principal onde ficarão as notas
    frame_notas = ctk.CTkFrame(root)
    frame_notas.place(relx=0.5, rely=0.5, relwidth=0.8, relheight=0.8, anchor='center')
    
    # Configurações de grid para centralizar o conteúdo
    frame_notas.grid_rowconfigure(0, weight=0)  # Título
    frame_notas.grid_rowconfigure(1, weight=1)  # Scroll frame
    frame_notas.grid_rowconfigure(2, weight=0)  # Botão Voltar
    for col in range(7):
        frame_notas.grid_columnconfigure(col, weight=1)

    # Título
    label_titulo = ctk.CTkLabel(
        frame_notas, 
        text="Notas do Aluno", 
        font=("Arial", 20, "bold")
    )
    label_titulo.grid(row=0, column=0, columnspan=7, pady=10, padx=10, sticky="ew")
    
    # Frame rolável para a tabela
    scroll_frame = ctk.CTkScrollableFrame(frame_notas)
    scroll_frame.grid(row=1, column=0, columnspan=7, sticky="nsew", padx=10, pady=10)

    # Configura as colunas do scroll_frame para centralizar o conteúdo
    for col in range(7):
        scroll_frame.grid_columnconfigure(col, weight=1)

    # Usaremos as colunas 1 a 5 para a tabela (colunas 0 e 6 ficam vazias para centralização)
    row_index = 0
    
    for id_curso in cursos:
        curso = dados['cursos'][id_curso]
        
        # Label do nome do curso centralizado nas colunas 1 a 5
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
        
        # Cabeçalho nas colunas 1 a 5
        for col, text in enumerate(headers, start=1):
            ctk.CTkLabel(
                scroll_frame, 
                text=text, 
                font=("Arial", 14, "bold"), 
                fg_color="#444", 
                text_color="white"
            ).grid(row=row_index, column=col, padx=5, pady=5, sticky="ew")
        row_index += 1
        
        for id_disciplina in curso['id_disciplinas']:
            disciplina = dados['disciplinas'][id_disciplina]
            # Lê as notas; se não existirem, assume [0, 0]
            notas_disciplina = dados['notas'][matricula].get(id_disciplina, [0, 0])
            media = (notas_disciplina[0] + notas_disciplina[1]) / 2
            
            # Coluna 1: Nome da disciplina
            ctk.CTkLabel(
                scroll_frame, 
                text=disciplina["nome"], 
                font=("Arial", 12)
            ).grid(row=row_index, column=1, padx=5, pady=5, sticky="ew")
            
            # Coluna 2: Entrada para Nota 1
            entrada_nota1 = ctk.CTkEntry(scroll_frame, width=80)
            entrada_nota1.insert(0, str(notas_disciplina[0]))
            entrada_nota1.grid(row=row_index, column=2, padx=5, pady=5)
            
            # Coluna 3: Entrada para Nota 2
            entrada_nota2 = ctk.CTkEntry(scroll_frame, width=80)
            entrada_nota2.insert(0, str(notas_disciplina[1]))
            entrada_nota2.grid(row=row_index, column=3, padx=5, pady=5)
            
            # Coluna 4: Média
            ctk.CTkLabel(
                scroll_frame, 
                text=f"{media:.2f}", 
                font=("Arial", 12, "bold"), 
                text_color="green"
            ).grid(row=row_index, column=4, padx=5, pady=5, sticky="ew")
            
            # Coluna 5: Botão Salvar, com captura dos widgets de entrada no lambda
            btn_salvar = ctk.CTkButton(
                scroll_frame, 
                text="Salvar", 
                command=lambda d=id_disciplina, c=id_curso, en1=entrada_nota1, en2=entrada_nota2: salvar_nota(root, matricula, c, d, en1, en2)
            )
            btn_salvar.grid(row=row_index, column=5, padx=5, pady=5)
            row_index += 1
    
    # Botão Voltar, abaixo do scroll_frame
    button_voltar = ctk.CTkButton(
        frame_notas, 
        text="Voltar", 
        command=lambda: dashboard.exibir_dashboard(root, matricula)
    )
    button_voltar.grid(row=2, column=0, columnspan=7, pady=10)
