import requests

def buscar_materiais(disciplina):
    url = f"https://api.exemplo.com/materiais?disciplina={disciplina}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Levanta um erro se o status code não for 200
        return response.json()  # Retorna os dados em formato JSON
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar materiais: {e}")
        return None
