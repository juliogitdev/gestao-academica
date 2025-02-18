import re

# Função para validar o nome
def validar_nome(nome):
    # Verifica se o nome contém apenas letras e espaços
    if bool(re.fullmatch(r"[A-Za-zÀ-ÖØ-öø-ÿ\s]+", nome)):
        return True, None  # Retorna True e None se for válido
    return False, {'error': 'Nome inválido'}  # Retorna False e a mensagem de erro se não for válido

# Função para validar a matrícula
def validar_matricula(matricula):
    # Verifica se a matrícula é numérica e tem pelo menos 5 caracteres
    if matricula.isdigit() and len(matricula) >= 5:
        return True, None  # Retorna True e None se for válido
    return False, {'error': 'Matrícula inválida'}  # Retorna False e a mensagem de erro se não for válido

# Função para validar o e-mail
def validar_email(email):
    # Verifica se o e-mail tem o formato adequado usando regex
    if bool(re.fullmatch(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email)):
        return True, None  # Retorna True e None se for válido
    return False, {'error': 'Email inválido'}  # Retorna False e a mensagem de erro se não for válido

# Função para validar a nota
def validar_nota(nota):
    # Verifica se a nota é um número (inteiro ou flutuante) entre 0 e 100
    if isinstance(nota, (int, float)) and 0 <= nota <= 100:
        return True, None  # Retorna True e None se for válido
    return False, {'error': 'Nota inválida'}  # Retorna False e a mensagem de erro se não for válida

# Função para validar o número da nota (Nota 1 ou Nota 2)
def validar_numero_nota(n_nota):
    # Verifica se o número da nota é 0 ou 1
    if n_nota in [0, 1]:
        return True, None  # Retorna True e None se for válido
    return False, {'error': 'Número da nota inválido'}  # Retorna False e a mensagem de erro se não for válido
