# Sistema de Gestão Acadêmica

Este sistema foi desenvolvido para permitir o gerenciamento de alunos, cursos e disciplinas em um ambiente acadêmico. Criado como parte de um projeto universitário no curso de **Sistemas para Internet** no **IF Sertão Central**, campus Salgueiro, o objetivo principal é fornecer uma plataforma simples e eficaz para controlar o perfil do aluno, as notas, os cursos em que ele está matriculado e as disciplinas associadas.

## Funcionalidades

- **Cadastro de Alunos:** Permite o cadastro de novos alunos, incluindo matrícula, nome e e-mail.
- **Cadastro de Cursos e Disciplinas:** Adiciona cursos aos alunos e disciplinas aos cursos.
- **Gerenciamento de Notas:** Controle de duas notas por disciplina.
- **Remoção de Alunos, Cursos e Disciplinas:** Possibilidade de remover alunos, cursos ou disciplinas.
- **Dashboard:** Visualização de informações sobre o desempenho do aluno e acesso a materiais gratuitos relacionados às matérias com dificuldade.

## Tecnologias Utilizadas

- **Python:** Linguagem de programação principal do projeto.
- **Tkinter:** Biblioteca usada para criar a interface gráfica do sistema.
- **JSON:** Para armazenamento de dados (como alunos, cursos e disciplinas) em um único arquivo.
- **PIP:** Para gerenciamento de dependências.

## Como Rodar o Projeto

### Pré-requisitos

Certifique-se de ter o **Python** instalado em sua máquina. Você pode verificar se o Python está instalado rodando o seguinte comando no terminal:

```bash
python --version
```
```bash
python rundev.py
```
```bash
python main.py
```
## Estrutura de Arquivos

- `rundev.py`: Script para instalar dependências e rodar o sistema.
- `main.py`: Arquivo principal do sistema (substitua com o nome correto).
- `data/data_base.json`: Arquivo onde os dados dos alunos, cursos e disciplinas são armazenados.
- `requirements.txt`: Arquivo contendo as dependências do projeto.

## Como Funciona

1. **Cadastro de Aluno:** O aluno é registrado com seu nome, matrícula e e-mail.
2. **Cadastro de Cursos:** Cursos são associados a alunos, e cada curso pode ter várias disciplinas.
3. **Gerenciamento de Notas:** O sistema permite registrar até duas notas por disciplina.
4. **Gerenciamento de Disciplinas e Cursos:** Disciplinas podem ser removidas e associadas a novos cursos.
5. **Verificação de Login:** O sistema verifica a matrícula e o e-mail do aluno para permitir o acesso.
