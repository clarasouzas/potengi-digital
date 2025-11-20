from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field, HTML
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from .models import Aluno

User = get_user_model()

# ==========================
# LOGIN COM E-MAIL
# ==========================
class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Seu e-mail"}),
    )


# ==========================
# CADASTRO DE ALUNO (ENXUTO)
# ==========================
class AlunoForm(forms.Form):
    nome = forms.CharField(label="Nome Completo", max_length=100)
    email = forms.EmailField(label="E-mail")
    curso = forms.ChoiceField(
        choices=[
            ("InfoWeb", "Informática para Internet"),
            ("Meio Ambiente", "Meio Ambiente"),
            ("Edificações", "Edificações"),
            ("Licenciatura em Matemática", "Licenciatura em Matemática"),
        ],
        label="Curso"
    )
    senha = forms.CharField(widget=forms.PasswordInput())
    confirmar_senha = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column("nome", css_class="col-12 mb-3"),
            ),
            Row(
                Column("email", css_class="col-12 mb-3"),
            ),
            Row(
                Column("curso", css_class="col-12 mb-3"),
            ),
            Row(
                Column("senha", css_class="col-6 mb-3"),
                Column("confirmar_senha", css_class="col-6 mb-3"),
            ),
        )


# ==========================
# CADASTRO DE EMPRESA (ENXUTO)
# ==========================
class EmpresaForm(forms.Form):
    nome_empresa = forms.CharField(label="Nome da Empresa", max_length=100)
    cnpj = forms.CharField(label="CNPJ", max_length=18)
    email = forms.EmailField(label="E-mail Corporativo")
    telefone = forms.CharField(label="Telefone", max_length=20)
    senha = forms.CharField(widget=forms.PasswordInput())
    confirmar_senha = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(Column("nome_empresa", css_class="mb-3"),
                Column("cnpj", css_class="mb-3"),
                ),
            Row(Column("email", css_class="mb-3")),
            Row(Column("telefone", css_class="mb-3")),
            Row(
                Column("senha", css_class="col-6 mb-3"),
                Column("confirmar_senha", css_class="col-6 mb-3"),
            ),
        )


# ==========================
# CADASTRO DE COORDENAÇÃO (ENXUTO)
# ==========================
class CoordenacaoForm(forms.Form):
    nome = forms.CharField(label="Nome Completo", max_length=100)
    email = forms.EmailField(label="E-mail Institucional")
    senha = forms.CharField(widget=forms.PasswordInput())
    confirmar_senha = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(Column("nome", css_class="mb-3")),
            Row(Column("email", css_class="mb-3")),
            Row(
                Column("senha", css_class="col-6 mb-3"),
                Column("confirmar_senha", css_class="col-6 mb-3"),
            ),
        )
