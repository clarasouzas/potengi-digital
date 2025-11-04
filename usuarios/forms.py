from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Aluno, Empresa


# =====================================================
# FORMULÁRIO BASE DE USUÁRIO
# =====================================================
class UsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ["email", "username", "tipo", "password1", "password2"]
        widgets = {
            "tipo": forms.Select(attrs={"class": "form-select"}),
        }


# =====================================================
# FORM DE ALUNO
# =====================================================
class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ["curso", "curriculo", "portfolio"]
        widgets = {
            "curso": forms.TextInput(attrs={"class": "form-control"}),
            "portfolio": forms.URLInput(attrs={"class": "form-control"}),
        }


# =====================================================
# FORM DE EMPRESA
# =====================================================
class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ["nome_fantasia", "cnpj", "area_atuacao", "endereco", "telefone", "site"]
        widgets = {
            "nome_fantasia": forms.TextInput(attrs={"class": "form-control"}),
            "cnpj": forms.TextInput(attrs={"class": "form-control"}),
            "area_atuacao": forms.TextInput(attrs={"class": "form-control"}),
            "endereco": forms.TextInput(attrs={"class": "form-control"}),
            "telefone": forms.TextInput(attrs={"class": "form-control"}),
            "site": forms.URLInput(attrs={"class": "form-control"}),
        }
