from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import (
    AlunoCreationForm,
    EmpresaCreationForm,
    CoordenadorCreationForm
)
from .models import Usuario, Aluno, Empresa, Coordenador


# =====================================================
# TELA INICIAL DO CADASTRO
# =====================================================
def cadastro(request):
    return render(request, "registration/cadastro.html", {
        "forms": [
            ("aluno", AlunoCreationForm(), "usuarios:cadastro_aluno", "bi-mortarboard-fill", "Cadastro de Aluno"),
            ("empresa", EmpresaCreationForm(), "usuarios:cadastro_empresa", "bi-building-fill", "Cadastro de Empresa"),
            ("coord", CoordenadorCreationForm(), "usuarios:cadastro_coord", "bi-person-gear", "Cadastro de Coordenação"),
        ],
        "active_tab": "aluno",
    })


# =====================================================
# CADASTRO — ALUNO
# =====================================================
def cadastro_aluno(request):
    if request.method == "POST":
        form = AlunoCreationForm(request.POST)

        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.tipo = "aluno"
            usuario.save()

            Aluno.objects.create(
                usuario=usuario,
                nome=form.cleaned_data["nome"],
                curso=form.cleaned_data["curso"],
            )

            messages.success(request, "Aluno cadastrado com sucesso!")
            return redirect("usuarios:login")

        # ERRO — VOLTA PRA ABA CORRETA SEM QUEBRAR CSS
        return render(request, "registration/cadastro.html", {
            "forms": [
                ("aluno", form, "usuarios:cadastro_aluno", "bi-mortarboard-fill", "Cadastro de Aluno"),
                ("empresa", EmpresaCreationForm(), "usuarios:cadastro_empresa", "bi-building-fill", "Cadastro de Empresa"),
                ("coord", CoordenadorCreationForm(), "usuarios:cadastro_coord", "bi-person-gear", "Cadastro de Coordenação"),
            ],
            "active_tab": "aluno",
        })


# =====================================================
# CADASTRO — EMPRESA
# =====================================================
def cadastro_empresa(request):
    if request.method == "POST":
        form = EmpresaCreationForm(request.POST)

        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.tipo = "empresa"
            usuario.save()

            Empresa.objects.create(
                usuario=usuario,
                nome_empresa=form.cleaned_data["nome_empresa"],
                cnpj=form.cleaned_data["cnpj"],
                telefone=form.cleaned_data["telefone"],
                cidade=form.cleaned_data["cidade"],
                descricao=form.cleaned_data.get("descricao", "")
            )

            messages.success(request, "Empresa cadastrada com sucesso!")
            return redirect("usuarios:login")

        return render(request, "registration/cadastro.html", {
            "forms": [
                ("aluno", AlunoCreationForm(), "usuarios:cadastro_aluno", "bi-mortarboard-fill", "Cadastro de Aluno"),
                ("empresa", form, "usuarios:cadastro_empresa", "bi-building-fill", "Cadastro de Empresa"),
                ("coord", CoordenadorCreationForm(), "usuarios:cadastro_coord", "bi-person-gear", "Cadastro de Coordenação"),
            ],
            "active_tab": "empresa",
        })


# =====================================================
# CADASTRO — COORDENAÇÃO
# =====================================================
def cadastro_coord(request):
    if request.method == "POST":
        form = CoordenadorCreationForm(request.POST)

        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.tipo = "coordenador"
            usuario.is_staff = True
            usuario.save()

            Coordenador.objects.create(
                usuario=usuario,
                nome=form.cleaned_data["nome"],
                setor=form.cleaned_data["setor"],
            )

            messages.success(request, "Coordenação cadastrada com sucesso!")
            return redirect("usuarios:login")

        return render(request, "registration/cadastro.html", {
            "forms": [
                ("aluno", AlunoCreationForm(), "usuarios:cadastro_aluno", "bi-mortarboard-fill", "Cadastro de Aluno"),
                ("empresa", EmpresaCreationForm(), "usuarios:cadastro_empresa", "bi-building-fill", "Cadastro de Empresa"),
                ("coord", form, "usuarios:cadastro_coord", "bi-person-gear", "Cadastro de Coordenação"),
            ],
            "active_tab": "coord",
        })
