from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from .models import Vaga, Candidatura, Mensagem


# =====================================================
# FORMULÁRIO DE VAGA (para empresas)
# =====================================================

class VagaForm(forms.ModelForm):
    class Meta:
        model = Vaga
        fields = [
            "titulo",
            "descricao",
            "requisitos",
            "area",
            "tipo",
            "remuneracao",
            "cidade",
            "estado",
            "bairro",
            "data_inicio",
            "data_fim",
        ]
        widgets = {
            "descricao": forms.Textarea(attrs={"rows": 3, "placeholder": "Descreva a vaga..."}),
            "requisitos": forms.Textarea(attrs={"rows": 3, "placeholder": "Informe os requisitos..."}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Row(
                Column("titulo", css_class="col-md-6"),
                Column("tipo", css_class="col-md-6"),
            ),
            Row(
                Column("descricao", css_class="col-12"),
            ),
            Row(
                Column("requisitos", css_class="col-12"),
            ),
            Row(
                Column("area", css_class="col-md-4"),
                Column("remuneracao", css_class="col-md-4"),
                Column("cidade", css_class="col-md-4"),
            ),
            Row(
                Column("estado", css_class="col-md-6"),
                Column("bairro", css_class="col-md-6"),
            ),
            Row(
                Column("data_inicio", css_class="col-md-6"),
                Column("data_fim", css_class="col-md-6"),
            ),
            Submit("submit", "Salvar Vaga", css_class="btn btn-primary mt-3"),
        )


# =====================================================
# FORMULÁRIO DE CANDIDATURA (para alunos)
# =====================================================

class CandidaturaForm(forms.ModelForm):
    class Meta:
        model = Candidatura
        fields = ["mensagem"]
        widgets = {
            "mensagem": forms.Textarea(
                attrs={"rows": 4, "placeholder": "Fale brevemente sobre seu interesse..."}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            "mensagem",
            Submit("submit", "Enviar Candidatura", css_class="btn btn-success mt-3"),
        )


# =====================================================
# FORMULÁRIO DE MENSAGEM (para comunicação interna)
# =====================================================

class MensagemForm(forms.ModelForm):
    class Meta:
        model = Mensagem
        fields = ["destinatario", "conteudo"]
        widgets = {
            "conteudo": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Digite sua mensagem..."}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["destinatario"].label = "Enviar para"
        self.fields["conteudo"].label = "Mensagem"
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Row(
                Column("destinatario", css_class="col-md-6"),
            ),
            Row(
                Column("conteudo", css_class="col-12"),
            ),
            Submit("submit", "Enviar", css_class="btn btn-primary mt-3"),
        )
