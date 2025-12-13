<img src="static/assets/img/logo.svg" width="300" height="150">

# Sobre o Projeto — Potengi Digital

O **Potengi Digital** é uma plataforma desenvolvida como projeto de extensão do  
**Instituto Federal de Educação, Ciência e Tecnologia do Rio Grande do Norte – Campus São Paulo do Potengi**.

Seu objetivo é aproximar a formação técnica do mercado de trabalho, conectando alunos e ex-alunos do curso Técnico em Informática para Internet às empresas e instituições parceiras da região do Potengi.

Além da divulgação de vagas de estágio e jovem aprendiz, a plataforma fortalece a visibilidade do curso, contribui para a inserção profissional dos estudantes egressos e apoia o desenvolvimento socioeconômico local por meio da tecnologia.

---

## Funcionalidades

- Cadastro e autenticação de diferentes perfis (alunos, ex-alunos, empresas e coordenação).  
- Aprovação de empresas e validação de vagas pela Coordenação de Extensão.  
- Publicação e gerenciamento de vagas de estágio e jovem aprendiz.  
- Criação e atualização de currículos digitais pelos estudantes.  
- Pesquisa e filtros de oportunidades por curso, área e localização.  
- Interface responsiva e moderna, adaptada a dispositivos móveis.  

---

## Tecnologias Utilizadas

[![SkillIcons](https://skillicons.dev/icons?i=js,py,html,css,django,bootstrap)](https://skillicons.dev)

---

## Equipe do Projeto

### **Discentes Desenvolvedores**
- Clara Souza  
- Joice Leilhany  
- Elayne Fernandes  

### **Orientadora**
- Prof.ª Fernanda Lígia    

> Este repositório faz parte do Projeto de Extensão **Potengi Digital**, alinhado ao PDI do IFRN e aos Objetivos de Desenvolvimento Sustentável (ODS 4, 8 e 9).

---

## Rodando
Siga as instruções abaixo para configurar o ambiente do projeto após clonar o repositório.

---

### 1. Criando e Ativando o Ambiente Virtual
```bash
python -m venv venv  
venv\Scripts\Activate.ps1
```

### 2. Instalando as Dependências
```bash
pip install -r requirements.txt  
```

### 3. Aplicando as Migrações
```bash
python manage.py migrate  
```

### 4. Criando um Superusuário
```bash
python manage.py createsuperuser  
```

Siga as instruções e defina um nome de usuário, e-mail e senha.

### 5. Executando o Servidor

```bash
python manage.py runserver  
```

### 6. Acessando o Django Admin

Abra o navegador e acesse:

```
http://127.0.0.1:8000/usuarios/login
```

Faça login com o superusuário criado anteriormente.

Agora o **LinkIF** está pronto para ser utilizado!
