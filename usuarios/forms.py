from django import forms
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper 
from crispy_forms.layout import Layout, Row, Column
from .models import Usuario
from linkif.models import PerfilFormacao
from validate_docbr import CNPJ
import re


# ============================================
#   FORMULÁRIO BASE DE USUÁRIO
# ============================================
class UsuarioCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ["email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['email', 'telefone', 'status_aprovacao']
# ============================================
#   CADASTRO — ALUNO
# ============================================
class AlunoCreationForm(UsuarioCreationForm):

    curso = forms.ChoiceField(
        choices=[], 
        required=True,
        widget=forms.Select(attrs={"class": "form-select"})
    )

    class Meta(UsuarioCreationForm.Meta):
        fields = ["curso", "username"] + UsuarioCreationForm.Meta.fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # remove helptext
        for field in self.fields.values():
            field.help_text = None

        # CARREGA OS CURSOS SOMENTE AGORA (evita erro de migração)
        self.fields["curso"].choices = [
            (p.nome, p.nome) for p in PerfilFormacao.objects.all()
        ]

        self.helper = FormHelper()
        self.helper.form_tag = False  

        self.helper.layout = Layout(
            Row(
                Column("email", css_class="col-md-12"),
            ),
            Row(
                Column("username", css_class="col-md-6"),
                Column("curso", css_class="col-md-6"),
            ),
            Row(
                Column("password1", css_class="col-md-6"),
                Column("password2", css_class="col-md-6"),
            )
        )


# ============================================
#   CADASTRO — EMPRESA
# ============================================
class EmpresaCreationForm(UsuarioCreationForm):
    cnpj = forms.CharField(max_length=18)
    telefone = forms.CharField(max_length=20)

    class Meta(UsuarioCreationForm.Meta):
        fields = ["username", "cnpj", "telefone"] + UsuarioCreationForm.Meta.fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.help_text = None

        self.helper = FormHelper()
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Row(
                Column("username", css_class="col-md-6"),                
                Column("telefone", css_class="col-md-6"),
            ),
            Row(
                Column("email", css_class="col-md-12"),
            ),
            Row(
                Column("cnpj", css_class="col-md-12"),
            ),
            Row(
                Column("password1", css_class="col-md-6"),
                Column("password2", css_class="col-md-6"),
            ),
        )

    # VALIDAR CNPJ
    def clean_cnpj(self):
        cnpj = self.cleaned_data.get("cnpj")
        validador = CNPJ()

        if not validador.validate(cnpj):
            raise forms.ValidationError("CNPJ inválido. Verifique e tente novamente.")

        return validador.mask(cnpj)

    # VALIDAR TELEFONE
    def clean_telefone(self):
        telefone = self.cleaned_data.get("telefone")
        padrao = r"^\(?\d{2}\)?\s?\d{5}-?\d{4}$"

        if not re.match(padrao, telefone):
            raise forms.ValidationError("Telefone inválido. Use (84) 99999-9999.")

        return telefone


# ============================================
#   EDIÇÃO — ALUNO
# ============================================
class AlunoEditForm(forms.ModelForm):
    curso = forms.ChoiceField(choices=[])

    class Meta:
        model = Usuario
        fields = ["username", "curso", "foto", "curriculo", "portfolio", "resumo"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["curso"].choices = [
            (p.nome, p.nome) for p in PerfilFormacao.objects.all()
        ]

# ============================================
#   EDIÇÃO — EMPRESA
# ============================================
class EmpresaEditForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ["username", "telefone", "cnpj", "cidade", "descricao", "foto"]

    # VALIDAR CNPJ
    def clean_cnpj(self):
        cnpj = self.cleaned_data.get("cnpj")
        validador = CNPJ()

        if not validador.validate(cnpj):
            raise forms.ValidationError("CNPJ inválido. Verifique e tente novamente.")

        return validador.mask(cnpj)

    # VALIDAR TELEFONE
    def clean_telefone(self):
        telefone = self.cleaned_data.get("telefone")
        padrao = r"^\(?\d{2}\)?\s?\d{5}-?\d{4}$"

        if not re.match(padrao, telefone):
            raise forms.ValidationError("Telefone inválido. Use (84) 99999-9999.")

        return telefone


# ============================================
#   EDIÇÃO — COORDENAÇÃO
# ============================================
class CoordenadorEditForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ["username", "setor"]


class UsuarioEditFormSimples(forms.ModelForm):

    STATUS_CHOICES = [
        (True, "Aprovado"),
        (False, "Reprovado"),
    ]

    is_approved = forms.ChoiceField(
        label="Status de aprovação",
        choices=STATUS_CHOICES,
        widget=forms.RadioSelect(attrs={"class": "status-radio"})
    )

    class Meta:
        model = Usuario
        fields = ["email", "tipo", "is_approved"]

    def save(self, commit=True):
        instancia = super().save(commit=False)

        aprovado = self.cleaned_data["is_approved"] == "True"

        # === ATUALIZA AMBOS OS CAMPOS ===
        instancia.is_approved = aprovado
        instancia.status_aprovacao = "aprovado" if aprovado else "reprovado"

        if commit:
            instancia.save()

        return instancia
