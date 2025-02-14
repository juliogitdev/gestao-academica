import re

def validar_nome(nome):
    return bool(re.fullmatch(r"[A-Za-zÀ-ÖØ-öø-ÿ\s]+", nome))

def validar_matricula(matricula):
    if matricula.isdigit():
        if len(matricula) >= 5:
            return True
    return False

def validar_email(email):
    return bool(re.fullmatch(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email))

def validar_nota(nota):
    return isinstance(nota, (int, float)) and 0 <= nota <= 100

def validar_numero_nota(n_nota):
    return n_nota in [0, 1]
