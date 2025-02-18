Sistema de Gestão Acadêmica
Este sistema foi desenvolvido para permitir o gerenciamento de alunos, cursos e disciplinas em um ambiente acadêmico. Ele foi criado como parte de um projeto universitário no curso de Sistemas para Internet no IF Sertão Central, campus Salgueiro. O objetivo principal é fornecer uma plataforma simples e eficaz para controlar o perfil do aluno, as notas, os cursos em que ele está matriculado e as disciplinas associadas.

Funcionalidades
Cadastro de Alunos: Permite o cadastro de novos alunos, incluindo matrícula, nome e e-mail.
Cadastro de Cursos e Disciplinas: Adiciona cursos aos alunos e disciplinas aos cursos.
Gerenciamento de Notas: O sistema permite o controle de duas notas por disciplina.
Remoção de Alunos, Cursos e Disciplinas: Possibilidade de remover alunos, cursos ou disciplinas.
Dashboard: Visualização de informações sobre o desempenho do aluno e acesso a materiais gratuitos relacionados às matérias com dificuldade.
Tecnologias Utilizadas
Python: Linguagem de programação principal do projeto.
Tkinter: Biblioteca usada para criar a interface gráfica do sistema.
JSON: Para armazenamento de dados (como alunos, cursos e disciplinas) em um arquivo.
PIP: Para gerenciamento de dependências.
Como Rodar o Projeto
Pré-requisitos
Certifique-se de ter o Python instalado em sua máquina. Você pode verificar se o Python está instalado rodando o seguinte comando no terminal:

bash
Copiar
Editar
python --version
Passo 1: Instalar Dependências
Este projeto utiliza dependências externas listadas no arquivo requirements.txt. Para instalar todas as dependências necessárias, execute o seguinte comando:

bash
Copiar
Editar
python rundev.py
O script rundev.py vai instalar automaticamente todas as dependências e iniciar o sistema.

Passo 2: Rodar o Sistema
O sistema será iniciado automaticamente após a instalação das dependências.

Se precisar rodar o sistema manualmente, execute o seguinte comando:

bash
Copiar
Editar
python main.py


Estrutura de Arquivos
rundev.py: Script para instalar dependências e rodar o sistema.
nome_do_seu_arquivo.py: Arquivo principal do sistema (substitua com o nome correto).
data/data_base.json: Arquivo onde os dados dos alunos, cursos e disciplinas são armazenados.
requirements.txt: Arquivo contendo as dependências do projeto.
Como Funciona
Cadastro de Aluno: O aluno é registrado com seu nome, matrícula e e-mail.
Cadastro de Cursos: Cursos são associados a alunos, e cada curso pode ter várias disciplinas.
Gerenciamento de Notas: O sistema permite registrar até duas notas por disciplina.
Gerenciamento de Disciplinas e Cursos: Disciplinas podem ser removidas e associadas a novos cursos.
Verificação de Login: O sistema verifica a matrícula e o e-mail do aluno para permitir o acesso.