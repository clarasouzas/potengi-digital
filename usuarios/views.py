from django.shortcuts import render

def index(request):
    return render(request, "usuarios/index.html")
def login(request):
    return render(request, "usuarios/login.html")
def cadastro_candidato(request):
    return render(request, "usuarios/cadastro_candidato.html")
def cadastro_empresa(request):
    return render(request, "usuarios/cadastro_empresa.html")
def vagas(request):
    return render(request, "usuarios/vagas.html")
def perfil_cursos(request):
    return render(request, "usuarios/perfil_cursos.html")