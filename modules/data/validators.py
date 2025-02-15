import re

def validar_nome(nome):
    if bool(re.fullmatch(r"[A-Za-zÀ-ÖØ-öø-ÿ\s]+", nome)):
        return True, None
    return False, {'error', 'Nome inválido'}

def validar_matricula(matricula):
    if matricula.isdigit():
        if len(matricula) >= 5:
            return True, None
    return False, {'error' 'Matricula inválida'}

def validar_email(email):
    if bool(re.fullmatch(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email)):
        return True, None
    return False, {'error' 'Email inválida'}

def validar_nota(nota):
    if isinstance(nota, (int, float)) and 0 <= nota <= 100:
        return True, None
    return False, {'error' 'Nota inválida'}

def validar_numero_nota(n_nota):
    if n_nota in [0, 1]:
        return True, None
    return False, {'error' 'Número da nota inválida'}

