from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CoordenacaoForm, AlunoForm, EmpresaForm
from .models import Usuario


# =====================================================
# CADASTRO DE USUÁRIO (Aluno, Empresa, Coordenação)
# =====================================================
def cadastro(request):
    form_aluno = AlunoForm()
    form_empresa = EmpresaForm()
    form_coord = CoordenacaoForm()
    return render(request, "registration/cadastro.html", {
        "form_aluno": form_aluno,
        "form_empresa": form_empresa,
        "form_coord": form_coord
    })

def cadastro_aluno(request):
    if request.method == "POST":
        form = AlunoForm(request.POST)
        if form.is_valid():
            messages.success(request, "Aluno cadastrado com sucesso!")
            return redirect("usuarios:login")
    return redirect("usuarios:cadastro")

def cadastro_empresa(request):
    if request.method == "POST":
        form = EmpresaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Empresa cadastrada com sucesso!")
            return redirect("usuarios:login")
    return redirect("usuarios:cadastro")

def cadastro_coord(request):
    if request.method == "POST":
        form = CoordenacaoForm(request.POST)
        if form.is_valid():
            messages.success(request, "Coordenação cadastrada com sucesso!")
            return redirect("usuarios:login")
    return redirect("usuarios:cadastro")