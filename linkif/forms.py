from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from .models import Vaga, Candidatura, MensagemContato


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
            "tipo",
            "remuneracao",
            "cidade",
            "bairro",
            "data_inicio",
            "data_fim",
        ]

        widgets = {
            "titulo": forms.TextInput(attrs={
                "class": "soft-input",
                "placeholder": "Ex: Desenvolvedor Front-End"
            }),

            "descricao": forms.Textarea(attrs={
                "class": "soft-textarea",
                "rows": 5,
                "placeholder": "Descreva as atividades, horário, benefícios..."
            }),

            "requisitos": forms.Textarea(attrs={
                "class": "soft-textarea",
                "rows": 4,
                "placeholder": "Ex: HTML, CSS, Git, comunicação..."
            }),

    

            "tipo": forms.Select(attrs={
                "class": "soft-input"
            }),

            "remuneracao": forms.NumberInput(attrs={
                "class": "soft-input",
                "placeholder": "Ex: 600.00"
            }),

            "cidade": forms.TextInput(attrs={
                "class": "soft-input",
                "placeholder": "Cidade da vaga"
            }),

        

            "bairro": forms.TextInput(attrs={
                "class": "soft-input",
                "placeholder": "Bairro"
            }),

            "data_inicio": forms.DateInput(attrs={
                "type": "date",
                "class": "soft-input"
            }),

            "data_fim": forms.DateInput(attrs={
                "type": "date",
                "class": "soft-input"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        obrigatorios = ["titulo", "descricao", "tipo", "cidade","remuneracao","data_inicio","data_fim"]    

        for campo in obrigatorios:
            self.fields[campo].required = True

    # labels
        self.fields["titulo"].label = "Título da Vaga *"
        self.fields["descricao"].label = "Descrição *"
        self.fields["requisitos"].label = "Requisitos"
        self.fields["tipo"].label = "Tipo"
        self.fields["remuneracao"].label = "Bolsa / Salário (R$)"
        self.fields["cidade"].label = "Cidade"
        self.fields["bairro"].label = "Bairro"
        self.fields["data_inicio"].label = "Início"
        self.fields["data_fim"].label = "Término"

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

from django import forms
from .models import MensagemContato

class ContatoForm(forms.ModelForm):
    class Meta:
        model = MensagemContato
        fields = ['nome', 'email', 'mensagem']

        labels = {
            'nome': 'Nome',
            'email': 'E-mail',
            'mensagem': 'Mensagem',
        }

        widgets = {
            'mensagem': forms.Textarea(attrs={'rows': 3}),
        }