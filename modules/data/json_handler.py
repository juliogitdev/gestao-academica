import os
import json

# Define o caminho do arquivo do script atual
caminho_local = os.path.abspath(__file__)

# Define o caminho do arquivo de banco de dados JSON
caminho_data_base = os.path.normpath(os.path.join(caminho_local, '..', '..', '..', 'data', 'data_base.json'))

# Função para carregar os dados do arquivo JSON
def carregar_dados():
    if os.path.exists(caminho_data_base):
        try:
            # Tenta abrir e carregar os dados do arquivo JSON
            with open(caminho_data_base, 'r', encoding='utf-8') as dados:
                return json.load(dados)
        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar JSON: {e}")
            return {}  # Retorna um dicionário vazio se ocorrer erro na decodificação
        except Exception as e:
            print(f"Erro inesperado: {e}")
            return {}  # Retorna um dicionário vazio em caso de erro genérico
    else:
        print("Arquivo não encontrado!")
        return {}  # Retorna um dicionário vazio se o arquivo não for encontrado

# Função para salvar os dados no arquivo JSON
def salvar_dados(dados):
    try:
        # Tenta abrir e salvar os dados no arquivo JSON
        with open(caminho_data_base, 'w', encoding='utf-8') as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)
            print("dados salvos com sucesso")
    except Exception as e:
        print(f"Erro ao salvar os dados. erro: {e}")

# Função para gerar um novo ID para entidades (cursos ou disciplinas)
def gerar_id(entidade):
    dados = carregar_dados()

    # Verifica se a entidade é cursos ou disciplinas
    if entidade == "cursos" or entidade == "disciplinas":
        dados_entidade = dados[entidade].keys()  # Pega as chaves (IDs) da entidade

        if not dados_entidade:  # Se não houver dados para a entidade, retorna o ID "1"
            print(f"Sem dados de {entidade}")
            return "1"

        # Caso contrário, retorna o maior ID existente + 1
        new_id = int(max(dados_entidade)) + 1
        return str(new_id)
    else:
        return print("Erro na entidade")  # Caso a entidade não seja cursos nem disciplinas

# Função para verificar se já existem registros em uma entidade
def verficiar_registro_entidade(entidade):
    dados = carregar_dados()

    try:
        # Verifica se a quantidade de dados da entidade é maior que zero
        qtd_dados_entidade = len(dados[entidade])
        if qtd_dados_entidade > 0:
            return True
        else:
            return False
    except:
        return print("Erro ao verificar se existe registro em entidade")

# Função para adicionar um aluno ao sistema
def adicionar_aluno(nome, matricula, email):
    dados = carregar_dados()

    # Verifica se a matrícula já está cadastrada
    if not matricula in dados['alunos']:
        # Se não estiver, adiciona o aluno no dicionário de alunos
        dados['alunos'][matricula] = {"nome": nome, "email": email, "cursos":[], "disciplinas": []}
        dados['notas'][matricula] = {}  # Adiciona uma entrada no dicionário de notas
        salvar_dados(dados)
        return True
    else:
        print(f"A matrícula {matricula} já existe.")
        return False  # Retorna False se a matrícula já existir

# Função para adicionar um curso ao sistema
def adicionar_curso(nome, matricula):
    id_curso = gerar_id("cursos")
    curso = {"nome":nome, "id_aluno":matricula, "id_disciplinas": []}
    dados = carregar_dados()

    if matricula in dados['alunos'].keys():
        dados['cursos'][id_curso] = curso
        dados['alunos'][matricula]['cursos'].append(id_curso)
        salvar_dados(dados)
        return print(f"Curso {nome} adicionado.")
    
    print("Dados inválido")  # Caso o aluno não seja encontrado

# Função para adicionar uma disciplina a um curso
def adicionar_disciplina(nome, id_curso):
    dados = carregar_dados()

    try:
        curso = dados['cursos'][id_curso]  # Obtém o curso associado ao ID
        id_disciplina = gerar_id("disciplinas")
        disciplina_nova = {"nome":nome, "id_curso":id_curso}
        dados['disciplinas'][id_disciplina] = disciplina_nova
        
        matricula_aluno = curso['id_aluno']
        aluno = dados['alunos'][matricula_aluno]

        aluno['disciplinas'].append(id_disciplina)  # Associa a disciplina ao aluno
        curso['id_disciplinas'].append(id_disciplina)  # Associa a disciplina ao curso

        dados['notas'][matricula_aluno][id_disciplina] = [0, 0]  # Inicializa as notas do aluno

    except:
        return print("Erro ao encontrar o curso para associar a disciplina")
    
    salvar_dados(dados)

# Função para gerenciar as notas do aluno em uma disciplina
def gerenciar_nota(matricula, disciplina, nota, n_nota):
    dados = carregar_dados()

    if n_nota > 1 or n_nota < 0:
        return print("Apenas nota 1 e nota 2 pode ser gerenciado")
    
    try:
        dados['notas'][matricula][disciplina][n_nota] = nota
        salvar_dados(dados)
    except:
        return print("Erro ao gerenciar as notas")

# Função para remover uma disciplina
def remover_disciplina(id_disciplina, save_automatic = True):
    dados = carregar_dados()

    try:
        disciplina = dados['disciplinas'][id_disciplina]
        curso = dados['cursos'][disciplina['id_curso']]
        aluno_id = curso['id_aluno']
        aluno_disciplinas = dados['alunos'][aluno_id]['disciplinas']
        
        del dados['notas'][aluno_id][id_disciplina]  # Remove as notas associadas à disciplina
        del dados['disciplinas'][id_disciplina]  # Remove a disciplina
        aluno_disciplinas.remove(id_disciplina)  # Remove a disciplina do aluno
        curso['id_disciplinas'].remove(id_disciplina)  # Remove a disciplina do curso
        
        print(f"Disciplina {disciplina['nome']} removida com sucesso!")
        if save_automatic:
            salvar_dados(dados)
        
        return dados
    
    except:
        print("ERRO AO REMOVER DISCIPLINA")

# Função para remover um curso
def remover_curso(id_curso, save_automatic = True):
    try:
        dados = carregar_dados()
        curso = dados['cursos'][id_curso]
        disciplinas_curso = dados['cursos'][id_curso]['id_disciplinas']
    
        for id_disciplina in disciplinas_curso:
            print("Removendo disciplina")
            dados = remover_disciplina(id_disciplina)  # Remove as disciplinas associadas ao curso
    
        aluno = dados['alunos'][curso['id_aluno']]
        aluno['cursos'].remove(id_curso)  # Remove o curso do aluno
        del dados['cursos'][id_curso]  # Remove o curso
        
        if save_automatic:
            salvar_dados(dados)
        return dados
    except:
        print("Erro ao remover curso")

# Função para remover um aluno do sistema
def remover_aluno(matricula):
    try:
        dados = carregar_dados()
        cursos = dados['alunos'][matricula]['cursos']
        
        for curso in cursos:
            print(curso)
            dados = remover_curso(curso)  # Remove os cursos do aluno
        
        del dados['alunos'][matricula]  # Remove o aluno
        del dados['notas'][matricula]  # Remove as notas do aluno
        salvar_dados(dados)
        print("Aluno Removido com sucesso")
        return dados
    
    except:
        print("Erro ao excluir aluno")

# Função para verificar se existem alunos cadastrados
def verificar_alunos():
    dados = carregar_dados()
    if dados['alunos']:
        return True
    return False

# Função para verificar o login de um aluno
def verificar_login(matricula, email):
    dados = carregar_dados()

    try:
        aluno = dados['alunos'][matricula]
        if email != aluno['email']:  # Verifica se o e-mail está correto
            return False, ["Error", "E-mail inválido."]
        
        return True, None

    except:
        return False, ["Error", "Matricula não cadastrada ou inválida."]

