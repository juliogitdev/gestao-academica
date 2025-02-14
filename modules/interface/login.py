import customtkinter as ctk

def tela_login(root):

    for widget in root.winfo_children():
        widget.destroy()

    tela_login = ctk.CTkFrame(root)
    tela_login.pack(fill="both", expand=True)

    frame_itens = ctk.CTkFrame(tela_login)
    frame_itens.place(relx = 0.5, rely=0.5, anchor="center")


    label_login = ctk.CTkLabel(frame_itens, text="Login", font=("Arial", 16, "bold"))
    label_login.pack(pady=10)


    input_matricula = ctk.CTkEntry(frame_itens, width=200, height=40, placeholder_text="Matricula")
    input_matricula.pack(pady=1, padx = 10)

    input_email = ctk.CTkEntry(frame_itens, width=200, height=40, placeholder_text="Email")
    input_email.pack(pady=1, padx = 10)

    botao_enviar = ctk.CTkButton(frame_itens, width=150, height=40, text="Entrar")
    botao_enviar.pack(pady=20)