from django import forms
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from .models import Usuario, Aluno, Empresa, Coordenador


# =====================================================
# FORM BASE DO USUÁRIO — APENAS EMAIL + SENHA
# =====================================================
class UsuarioCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ["email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False  

# =====================================================
# FORM — ALUNO
# =====================================================
class AlunoCreationForm(UsuarioCreationForm):
    nome = forms.CharField(max_length=100)
    curso = forms.CharField(max_length=100)

    class Meta(UsuarioCreationForm.Meta):
        fields = ["nome", "curso"] + UsuarioCreationForm.Meta.fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False 

# =====================================================
# FORM — EMPRESA
# =====================================================
class EmpresaCreationForm(UsuarioCreationForm):
    nome_empresa = forms.CharField(max_length=150)
    cnpj = forms.CharField(max_length=18)
    telefone = forms.CharField(max_length=20)
    cidade = forms.CharField(max_length=100)
    descricao = forms.CharField(required=False, widget=forms.Textarea)

    class Meta(UsuarioCreationForm.Meta):
        fields = [
            "nome_empresa", "cnpj", "telefone", "cidade", "descricao"
        ] + UsuarioCreationForm.Meta.fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


# =====================================================
# FORM — COORDENAÇÃO
# =====================================================
class CoordenadorCreationForm(UsuarioCreationForm):
    nome = forms.CharField(max_length=100)
    setor = forms.CharField(max_length=100)

    class Meta(UsuarioCreationForm.Meta):
        fields = ["nome", "setor"] + UsuarioCreationForm.Meta.fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
class AlunoEditForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ["nome", "curso", "portfolio", "foto", "curriculo"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
class EmpresaEditForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ["nome_empresa", "telefone", "cidade", "descricao", "foto"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
class CoordenadorEditForm(forms.ModelForm):
    class Meta:
        model = Coordenador
        fields = ["nome", "setor"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
class UsuarioEditFormSimples(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ["email", "tipo", "is_approved"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # estilização
        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "form-control"
            })