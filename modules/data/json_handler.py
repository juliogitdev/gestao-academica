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

def gerar_id(entidade):
    dados = carregar_dados()

    #verifica se está tentando gerar id para disciplina ou curso
    if entidade == "cursos" or entidade == "disciplinas":
        #pega as chaves(id) das entidades(disciplina ou curso) e armazena em uma lista
        dados_entidade = dados[entidade].keys()

        #caso não tenha dado dentro da entidade ele retorna 1 para o primeiro id
        if not dados_entidade:
            print(f"Sem dados de {entidade}")
            return "1"
        
        #pega o maior id e iterar 1
        new_id = int(max(dados_entidade)) + 1

        #retorna o id gerado em formato de string
        return str(new_id)
        
    else:
        return print("Erro na entidade")

#verifica se a entidade já tem registro
def verficiar_registro_entidade(entidade):
    dados = carregar_dados()

    try:
        qtd_dados_entidade = len(dados[entidade])
        if qtd_dados_entidade > 0:
            return True
        else:
            return False
    except:
        return print("Erro ao verificar se existe registro em entidade")

#Adiciona um perfil
def adicionar_aluno(nome, matricula, email):
    dados = carregar_dados()

    #verifica se a matricula ja está cadastrada
    if not matricula in dados['alunos']:
        #adiciona na chave alunos outro dicionario com a chave sendo a matricula do aluno e o valor os dados do aluno
        dados['alunos'][matricula] = {"nome": nome, "email": email, "cursos":[], "disciplinas": []}
        #adiciona no dicionatio de notas outro dicionario com a chave sendo a matricula do aluno
        dados['notas'][matricula] = {}
        salvar_dados(dados)
        return True
    else:
        print(f"A matrícula {matricula} já existe.")
        return False


def adicionar_curso(nome, matricula):
    id_curso = gerar_id("cursos")
    curso = {"nome":nome, "id_aluno":matricula, "id_disciplinas": []}
    dados = carregar_dados()
    if matricula in dados['alunos'].keys():
        dados['cursos'][id_curso] = curso
        dados['alunos'][matricula]['cursos'].append(id_curso)

        salvar_dados(dados)
        return print(f"Curso {nome} adicionado.")
    
    print("Dados inválido")


def adicionar_disciplina(nome, id_curso):
    dados = carregar_dados()
    
    try:
        curso = dados['cursos'][id_curso]
        id_disciplina = gerar_id("disciplinas")
        disciplina_nova = {"nome":nome, "id_curso":id_curso}
        dados['disciplinas'][id_disciplina] = disciplina_nova
        
        matricula_aluno = curso['id_aluno']
        aluno = dados['alunos'][matricula_aluno]

        aluno['disciplinas'].append(id_disciplina)
        curso['id_disciplinas'].append(id_disciplina)

        dados['notas'][matricula_aluno][id_disciplina] = [0, 0]
        

    except:
        return print("Erro ao encontrar o curso para associar a disciplina")
    
    salvar_dados(dados)
    
def gerenciar_nota(matricula, disciplina, nota, n_nota):
    dados = carregar_dados()

    if n_nota > 1 or n_nota < 0:
        return print("Apenas nota 1 e nota 2 pode ser gerenciado")
    try:
        dados['notas'][matricula][disciplina][n_nota] = nota

        salvar_dados(dados)
    except:
        return print("Erro ao gerenciar as notas")


def remover_disciplina(id_disciplina, save_automatic = True):
    dados = carregar_dados()

    try:
        disciplina = dados['disciplinas'][id_disciplina]
        
        curso = dados['cursos'][disciplina['id_curso']]

        aluno_id = curso['id_aluno']
        aluno_disciplinas = dados['alunos'][aluno_id]['disciplinas']
        
        del dados['notas'][aluno_id][id_disciplina]
        del dados['disciplinas'][id_disciplina]
        aluno_disciplinas.remove(id_disciplina)
        curso['id_disciplinas'].remove(id_disciplina)
        
        print(f"Disciplina {disciplina['nome']} removida com sucesso!")
        if save_automatic:
            salvar_dados(dados)
        
        return dados
        
    
    except:
        print("ERRO AO REMOVER DISCIPLINA")

def remover_curso(id_curso, save_automatic = True):
    try:
        dados = carregar_dados()
        curso = dados['cursos'][id_curso]
        disciplinas_curso = dados['cursos'][id_curso]['id_disciplinas']
    
        for id_disciplina in disciplinas_curso:
            dados = remover_disciplina(id_disciplina, False)
    
        aluno = dados['alunos'][curso['id_aluno']]
    
        aluno['cursos'].remove(id_curso)
        del dados['cursos'][id_curso]

        if save_automatic:
            salvar_dados(dados)
        return dados
    except:
        print("Erro ao remover curso")

def remover_aluno(matricula):
    try:
        dados = carregar_dados()
        cursos = dados['alunos'][matricula]['cursos']
        for curso in cursos:
            dados = remover_curso(curso, False)

        del dados['alunos'][matricula]
        del dados['notas'][matricula]
        salvar_dados(dados)
        print("Aluno Removido com sucesso")
        return dados
    
    except:
        print("Erro ao excluir aluno")


def verificar_alunos():
    dados = carregar_dados()
    if dados['alunos']:
        return True
    
    return False

