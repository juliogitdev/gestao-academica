import customtkinter as ctk

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
    input_matricula.pack(pady=1, padx = 10)

    input_nome = ctk.CTkEntry(frame_itens, width=200, height=40, placeholder_text="Nome completo")
    input_nome.pack(pady=1, padx = 10)

    input_email = ctk.CTkEntry(frame_itens, width=200, height=40, placeholder_text="Email")
    input_email.pack(pady=1, padx = 10)

    botao_enviar = ctk.CTkButton(frame_itens, width=150, height=40, text="Cadastrar")
    botao_enviar.pack(pady=20)