import customtkinter as ctk
from tkinter import messagebox
from modules.data import json_handler, validators

def logar_aluno(input_matricula, input_email):
    matricula = input_matricula.get()
    email = input_email.get()

    

    if validators.validar_email(email) and validators.validar_matricula(matricula):
        autorizaçao_login, error = json_handler.verificar_login(matricula, email)
        if not autorizaçao_login:
            return messagebox.showerror(error[0], error[1])
        
        return messagebox.showinfo('Sucesso', "Sucesso ao entrar!")

    return messagebox.showerror(error[0], error[1])


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
    input_matricula.pack(pady=3, padx = 10)

    input_email = ctk.CTkEntry(frame_itens, width=200, height=40, placeholder_text="Email")
    input_email.pack(pady=3, padx = 10)

    botao_enviar = ctk.CTkButton(frame_itens, width=150, height=40, text="Entrar", command=lambda: logar_aluno(input_matricula, input_email))
    botao_enviar.pack(pady=20)