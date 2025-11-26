from django import forms
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from .models import Usuario


# ======================================
# FORM BASE — EMAIL + SENHA
# ======================================
class UsuarioCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ["email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


# ======================================
# CADASTRO — ALUNO
# ======================================
class AlunoCreationForm(UsuarioCreationForm):
    nome = forms.CharField(max_length=120)
    curso = forms.CharField(max_length=100)

    class Meta(UsuarioCreationForm.Meta):
        fields = ["nome", "curso"] + UsuarioCreationForm.Meta.fields


# ======================================
# CADASTRO — EMPRESA
# ======================================
class EmpresaCreationForm(UsuarioCreationForm):
    nome = forms.CharField(label="Nome da empresa", max_length=150)
    cnpj = forms.CharField(max_length=18)
    telefone = forms.CharField(max_length=20)
    cidade = forms.CharField(max_length=100)
    descricao = forms.CharField(required=False, widget=forms.Textarea)

    class Meta(UsuarioCreationForm.Meta):
        fields = [
            "nome", "cnpj", "telefone", "cidade", "descricao"
        ] + UsuarioCreationForm.Meta.fields


# ======================================
# EDIÇÃO — ALUNO
# ======================================
class AlunoEditForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ["nome", "curso", "foto", "curriculo", "portfolio"]


# ======================================
# EDIÇÃO — EMPRESA
# ======================================
class EmpresaEditForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ["nome", "telefone", "cidade", "descricao", "foto"]


# ======================================
# EDIÇÃO — COORDENAÇÃO
# ======================================
class CoordenadorEditForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ["nome", "setor"]


# ======================================
# EDIÇÃO — ADMIN (EMAIL | TIPO | APROVAÇÃO)
# ======================================
class UsuarioEditFormSimples(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ["email", "tipo", "is_approved"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            f.widget.attrs.update({"class": "form-control"})
