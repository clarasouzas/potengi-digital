from django.shortcuts import render

def index(request):
    return render(request, "linkif/index.html")
def login(request):
    return render(request, "linkif/login.html")
def cadastro(request):
    return render(request, "linkif/cadastro.html")

def vagas(request):
    return render(request, "linkif/vagas.html")
def perfil_cursos(request):
    return render(request, "linkif/perfil_cursos.html")
def vagas(request):
    return render(request, 'linkif/vagas.html')
def detalhar(request):
    return render(request, 'linkif/detalhar.html')