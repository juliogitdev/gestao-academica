import os
import sys
import subprocess

def instalar_dependencias():
    print("🔄 Instalando dependências...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("✅ Dependências instaladas com sucesso!\n")

def rodar_sistema():
    print("🚀 Iniciando o sistema...\n")
    os.system("python nome_do_seu_arquivo.py")  # Substitua pelo nome correto do seu programa

if __name__ == "__main__":
    instalar_dependencias()
    rodar_sistema()
