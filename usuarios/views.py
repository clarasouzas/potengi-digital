from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages

from .forms import (
    AlunoCreationForm,
    EmpresaCreationForm,
)
from .models import Usuario
def cadastro(request):
    return render(request, "registration/cadastro.html", {
        "forms": [
            ("aluno", AlunoCreationForm(), "usuarios:cadastro_aluno"),
            ("empresa", EmpresaCreationForm(), "usuarios:cadastro_empresa"),
        ],
        "active_tab": "aluno",
    })
def cadastro_aluno(request):
    if request.method == "POST":
        form = AlunoCreationForm(request.POST, request.FILES)

        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.tipo = "aluno"
            usuario.save()

            messages.success(request, "Cadastro de aluno realizado com sucesso!")
            return redirect("usuarios:login")

        return render(request, "registration/cadastro.html", {
            "forms": [
                ("aluno", form, "usuarios:cadastro_aluno"),
                ("empresa", EmpresaCreationForm(), "usuarios:cadastro_empresa"),
            ],
            "active_tab": "aluno",
        })

    return redirect("usuarios:cadastro")
def cadastro_empresa(request):
    if request.method == "POST":
        form = EmpresaCreationForm(request.POST, request.FILES)

        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.tipo = "empresa"
            usuario.save()

            messages.success(request, "Cadastro de empresa realizado com sucesso!")
            return redirect("usuarios:login")

        return render(request, "registration/cadastro.html", {
            "forms": [
                ("aluno", AlunoCreationForm(), "usuarios:cadastro_aluno"),
                ("empresa", form, "usuarios:cadastro_empresa"),
            ],
            "active_tab": "empresa",
        })

    return redirect("usuarios:cadastro")
def redirecionar_dashboard(request):
    user = request.user

    if user.tipo == "aluno":
        return redirect("dashboard:aluno_painel")

    if user.tipo == "empresa":
        return redirect("dashboard:empresa")

    if user.tipo == "coordenador":
        return redirect("dashboard:coord")

    return redirect("index")
