from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from allauth.socialaccount.models import SocialAccount

from .forms import (
    AlunoCreationForm,
    EmpresaCreationForm,
    AlunoEditForm,
    EmpresaEditForm,
)
from .models import Usuario

User = get_user_model()

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

            messages.success(request, "Cadastro realizado com sucesso!")
            messages.success(request, "Cadastro realizado com sucesso!")
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

            messages.success(request, "Cadastro realizado com sucesso!")
            messages.success(request, "Cadastro realizado com sucesso!")
            return redirect("usuarios:login")

        return render(request, "registration/cadastro.html", {
            "forms": [
                ("aluno", AlunoCreationForm(), "usuarios:cadastro_aluno"),
                ("empresa", form, "usuarios:cadastro_empresa"),
            ],
            "active_tab": "empresa",
        })

    return redirect("usuarios:cadastro")

@login_required
def completar_cadastro(request):
    user = request.user
    
    social_account = SocialAccount.objects.filter(user=user).first()
    if not social_account:
        return redirect('usuarios:redirecionar_dashboard')
    
    provider = social_account.provider
    
    if provider == 'google':
        if user.tipo == 'aluno' and user.curso:
            return redirect('usuarios:redirecionar_dashboard')
        
        if user.tipo == 'empresa' and user.telefone and user.cidade:
            return redirect('usuarios:redirecionar_dashboard')
    
    if request.method == "POST":
        if user.tipo == 'aluno':
            from .forms import AlunoEditForm
            form = AlunoEditForm(request.POST, request.FILES, instance=user)
        elif user.tipo == 'empresa':
            from .forms import EmpresaEditForm
            form = EmpresaEditForm(request.POST, request.FILES, instance=user)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Cadastro finalizado com sucesso. Bem-vindo!")
            return redirect('usuarios:redirecionar_dashboard')
    
    else:
        if user.tipo == 'aluno':
            from .forms import AlunoEditForm
            form = AlunoEditForm(instance=user)
        elif user.tipo == 'empresa':
            from .forms import EmpresaEditForm
            form = EmpresaEditForm(instance=user)
    
    context = {
        'form': form,
        'tipo': user.tipo,
        'provider': provider,
        'email': user.email,
        'foto': social_account.get_avatar_url(),
    }
    
    return render(request, "registration/completar_cadastro.html", context)

@login_required
def redirecionar_dashboard(request):
    user = request.user

    if user.tipo == "aluno":
        return redirect("dashboard:aluno_painel")

    if user.tipo == "empresa":
        return redirect("dashboard:empresa_painel")

    if user.tipo == "coordenador":
        return redirect("dashboard:coordenacao_painel")

    return redirect("index")

def social_login_callback(request):
    tipo = request.POST.get('tipo')
    
    if tipo in ['aluno', 'empresa']:
        request.session['social_login_type'] = tipo
        request.session.modified = True
        
        return JsonResponse({
            'success': True,
            'message': f'Tipo {tipo} definido na sessão'
        })
    
    return JsonResponse({
        'success': False,
        'error': 'Tipo inválido'
    })