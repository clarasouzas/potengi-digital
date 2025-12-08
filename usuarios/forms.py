from django import forms
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper 
from crispy_forms.layout import Layout, Row, Column, Field
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
    curso = forms.CharField(max_length=100)

    class Meta(UsuarioCreationForm.Meta):
        fields = ["curso", "username"] + UsuarioCreationForm.Meta.fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields.values():
            field.help_text = None
        self.helper = FormHelper()
        self.helper.form_tag = False  # não gera <form>

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


# ======================================
# CADASTRO — EMPRESA
# ======================================

class EmpresaCreationForm(UsuarioCreationForm):
    cnpj = forms.CharField(max_length=18)
    telefone = forms.CharField(max_length=20)

    class Meta(UsuarioCreationForm.Meta):
        fields = [
            "username", "cnpj", "telefone", 
        ] + UsuarioCreationForm.Meta.fields

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

# ======================================
# EDIÇÃO — ALUNO
# ======================================
class AlunoEditForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ["username", "curso", "foto", "curriculo", "portfolio","resumo"]


# ======================================
# EDIÇÃO — EMPRESA
# ======================================
class EmpresaEditForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ["username", "telefone", "cidade", "descricao", "foto"]


# ======================================
# EDIÇÃO — COORDENAÇÃO
# ======================================
class CoordenadorEditForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ["username", "setor"]

# ======================================
# EDIÇÃO — ADMIN (EMAIL | TIPO | APROVAÇÃO)
# ======================================
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # estilos dos campos normais
        for f_name, f in self.fields.items():
            if f_name != "is_approved":   # evita quebrar o RadioSelect
                f.widget.attrs.update({"class": "form-control"})
