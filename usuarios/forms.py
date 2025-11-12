from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field, HTML
from .models import Empresa
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(attrs={"autofocus": True, "class": "form-control"}),
    )

    class Meta:
        model = User
        fields = ["username", "password"]
# =====================================================
# FORMULÁRIO DE EMPRESA — LIMPO E PROFISSIONAL
# =====================================================
class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = [
            "nome_empresa", "razao_social", "cnpj", "setor", "tamanho_empresa",
            "telefone", "email", "cidade", "cep", "descricao"
        ]
        labels = {
            "nome_empresa": "Nome Fantasia",
            "razao_social": "Razão Social",
            "cnpj": "CNPJ",
            "setor": "Setor de Atuação",
            "tamanho_empresa": "Porte da Empresa",
            "telefone": "Telefone de Contato",
            "email": "E-mail Corporativo",
            "cidade": "Cidade",
            "cep": "CEP",
            "descricao": "Descrição da Empresa",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_tag = False

        self.helper.layout = Layout(
            HTML("<h6 class='titulo-section mb-3'>Informações da Empresa</h6>"),
            Row(
                Column("nome_empresa", css_class="col-md-6 mb-3"),
                Column("razao_social", css_class="col-md-6 mb-3"),
            ),
            Row(
                Column("cnpj", css_class="col-md-4 mb-3"),
                Column("setor", css_class="col-md-4 mb-3"),
                Column("tamanho_empresa", css_class="col-md-4 mb-3"),
            ),

            HTML("<h6 class='titulo-section mt-4 mb-3'>Contato</h6>"),
            Row(
                Column("telefone", css_class="col-md-6 mb-3"),
                Column("email", css_class="col-md-6 mb-3"),
            ),

            HTML("<h6 class='titulo-section mt-4 mb-3'>Localização</h6>"),
            Row(
                Column("cidade", css_class="col-md-8 mb-3"),
                Column("cep", css_class="col-md-4 mb-3"),
            ),

            HTML("<h6 class='titulo-section mt-4 mb-3'>Sobre</h6>"),
            Field("descricao", css_class="mb-3"),
        )


# =====================================================
# FORMULÁRIO DE ALUNO — ORGANIZADO E HARMONIOSO
# =====================================================
class AlunoForm(forms.Form):
    nome = forms.CharField(label="Nome Completo", max_length=100)
    matricula = forms.CharField(label="Matrícula", max_length=20)
    curso = forms.ChoiceField(
        choices=[
            ("InfoWeb", "Informática para Internet"),
            ("Meio Ambiente", "Meio Ambiente"),
            ("Edificações", "Edificações"),
            ("Licenciatura em Matemática", "Licenciatura em Matemática"),
        ],
        label="Curso"
    )
    email = forms.EmailField(label="E-mail Acadêmico")
    senha = forms.CharField(label="Senha", widget=forms.PasswordInput)
    confirmar_senha = forms.CharField(label="Confirmar Senha", widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_tag = False

        self.helper.layout = Layout(
            HTML("<h6 class='titulo-section mb-3'>Dados Pessoais</h6>"),
            Row(
                Column("nome", css_class="col-md-6 mb-3"),
                Column("matricula", css_class="col-md-6 mb-3"),
            ),

            HTML("<h6 class='titulo-section mt-4 mb-3'>Curso e Contato</h6>"),
            Row(
                Column("curso", css_class="col-md-6 mb-3"),
                Column("email", css_class="col-md-6 mb-3"),
            ),

            HTML("<h6 class='titulo-section mt-4 mb-3'>Acesso</h6>"),
            Row(
                Column("senha", css_class="col-md-6 mb-3"),
                Column("confirmar_senha", css_class="col-md-6 mb-3"),
            ),
        )


# =====================================================
# FORMULÁRIO DE COORDENAÇÃO — CLEAN E FUNCIONAL
# =====================================================
class CoordenacaoForm(forms.Form):
    nome = forms.CharField(label="Nome Completo", max_length=100)
    email = forms.EmailField(label="E-mail Institucional")
    cargo = forms.CharField(label="Cargo", max_length=80)
    departamento = forms.CharField(label="Departamento", max_length=100)
    senha = forms.CharField(label="Senha", widget=forms.PasswordInput)
    confirmar_senha = forms.CharField(label="Confirmar Senha", widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_tag = False

        self.helper.layout = Layout(
            HTML("<h6 class='titulo-section mb-3'>Informações Gerais</h6>"),
            Row(
                Column("nome", css_class="col-md-6 mb-3"),
                Column("email", css_class="col-md-6 mb-3"),
            ),

            HTML("<h6 class='titulo-section mt-4 mb-3'>Cargo e Departamento</h6>"),
            Row(
                Column("cargo", css_class="col-md-6 mb-3"),
                Column("departamento", css_class="col-md-6 mb-3"),
            ),

            HTML("<h6 class='titulo-section mt-4 mb-3'>Acesso</h6>"),
            Row(
                Column("senha", css_class="col-md-6 mb-3"),
                Column("confirmar_senha", css_class="col-md-6 mb-3"),
            ),
        )
