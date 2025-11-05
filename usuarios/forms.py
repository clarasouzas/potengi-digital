from django import forms
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field, HTML
from .models import Empresa


# ======================
# FORMULÁRIO DE EMPRESA
# ======================
class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = [
            "nome_empresa", "razao_social", "cnpj", "setor", "tamanho_empresa",
            "telefone", "email", "site", "logradouro", "bairro",
            "cidade", "estado", "cep", "descricao", "logo"
        ]
        labels = {
            "nome_empresa": "Nome Fantasia",
            "razao_social": "Razão Social",
            "cnpj": "CNPJ",
            "setor": "Setor de Atuação",
            "tamanho_empresa": "Porte da Empresa",
            "telefone": "Telefone de Contato",
            "email": "E-mail Corporativo",
            "site": "Site (opcional)",
            "logradouro": "Logradouro",
            "bairro": "Bairro",
            "cidade": "Cidade",
            "estado": "Estado (UF)",
            "cep": "CEP",
            "descricao": "Descrição da Empresa",
            "logo": "Logo (imagem opcional)",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column("nome_empresa", css_class="col-md-6 mb-3"),
                Column("razao_social", css_class="col-md-6 mb-3"),
            ),
            Row(
                Column("cnpj", css_class="col-md-4 mb-3"),
                Column("setor", css_class="col-md-4 mb-3"),
                Column("tamanho_empresa", css_class="col-md-4 mb-3"),
            ),
            Row(
                Column("telefone", css_class="col-md-6 mb-3"),
                Column("email", css_class="col-md-6 mb-3"),
            ),
            Row(
                Column("site", css_class="col-md-6 mb-3"),
                Column("logo", css_class="col-md-6 mb-3"),
            ),
            HTML("<h6 class='mt-3 text-primary'>Endereço</h6>"),
            Row(
                Column("logradouro", css_class="col-md-6 mb-3"),
                Column("bairro", css_class="col-md-6 mb-3"),
            ),
            Row(
                Column("cidade", css_class="col-md-4 mb-3"),
                Column("estado", css_class="col-md-4 mb-3"),
                Column("cep", css_class="col-md-4 mb-3"),
            ),
            Field("descricao", css_class="mb-3"),
        )


# ======================
# FORMULÁRIO DE ALUNO
# ======================
class AlunoForm(forms.Form):
    nome = forms.CharField(label="Nome Completo", max_length=100)
    matricula = forms.CharField(label="Matrícula", max_length=20)
    curso = forms.ChoiceField(
        choices=[
            ("InfoWeb", "Informática para Internet"),
            ("Administração", "Administração"),
            ("Eletrotécnica", "Eletrotécnica"),
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
            Row(
                Column("nome", css_class="col-md-6 mb-3"),
                Column("matricula", css_class="col-md-6 mb-3"),
            ),
            Row(
                Column("curso", css_class="col-md-6 mb-3"),
                Column("email", css_class="col-md-6 mb-3"),
            ),
            Row(
                Column("senha", css_class="col-md-6 mb-3"),
                Column("confirmar_senha", css_class="col-md-6 mb-3"),
            )
        )


# ======================
# FORMULÁRIO DE COORDENAÇÃO
# ======================
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
            Row(
                Column("nome", css_class="col-md-6 mb-3"),
                Column("email", css_class="col-md-6 mb-3"),
            ),
            Row(
                Column("cargo", css_class="col-md-6 mb-3"),
                Column("departamento", css_class="col-md-6 mb-3"),
            ),
            Row(
                Column("senha", css_class="col-md-6 mb-3"),
                Column("confirmar_senha", css_class="col-md-6 mb-3"),
            )
        )
