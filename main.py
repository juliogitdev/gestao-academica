import customtkinter as ctk
from modules.data import json_handler
from modules.interface import cadastro_aluno, login, dashboard
import config



def iniciar_app():
    ctk.set_appearance_mode(config.TEMA) 
    ctk.set_default_color_theme(config.TEMA_COR)
    root = ctk.CTk()
    
    root.title("Sistema Gestão Acadêmica")
    
    root.geometry("800x600")  # Define as dimensões iniciais da janela
    #root.resizable(False, False) # Desativa o redimensionamento do sistema


    

    # Verifica se já existe aluno cadastrado no sistema para selecionar a tela inicial
    if json_handler.verificar_alunos():
        login.tela_login(root)
    else:
        cadastro_aluno.tela_cadastro_aluno(root)

    root.mainloop()


if __name__ =="__main__":
    iniciar_app()
