import os
import json

caminho_local = os.path.abspath(__file__)

caminho_data_base = os.path.normpath(os.path.join(caminho_local, '..', '..', '..', 'data', 'data_base.json'))

#Retorna os dados do arquivo json
def carregar_dados():

    if os.path.exists(caminho_data_base):

        try:
            with open(caminho_data_base, 'r', encoding='utf-8') as dados:
                return json.load(dados)
            
        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar JSON: {e}")
            return {}
        except Exception as e:
            print(f"Erro inesperado: {e}")
            return {}
    else:
        print("Arquivo não encontrado!")
        return {}  # Retorna um dicionário vazio se o arquivo não for encontrado
    
def salvar_dados(dados):

    try:
        with open(caminho_data_base, 'w', encoding='utf-8') as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)
            print("dados salvos com sucesso")
    except Exception as e:
        print(f"Erro ao salvar os dados. erro: {e}")

#Adiciona um perfil
def adicionar_aluno(nome, matricula, email):
    dados = carregar_dados()

    if not matricula in dados['alunos']:
        dados['alunos'][matricula] = {"nome": nome, "email": email, "cursos":[], "disciplinas": []}
        dados['notas'][matricula] = {}
        salvar_dados(dados)
        return True
    else:
        print(f"A matrícula {matricula} já existe.")
        return False

adicionar_aluno("julio", 516561, "julio@gmail.com")
