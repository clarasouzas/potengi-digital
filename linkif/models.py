from django.db import models
from django.conf import settings
from django.utils import timezone


# =====================================================
# PERFIS DE FORMAÇÃO (Curso)
# =====================================================
class PerfilFormacao(models.Model):
    nome = models.CharField("Nome do Curso", max_length=120, unique=True)
    descricao = models.TextField("Descrição", blank=True)
    descricao_curta = models.CharField("Descrição Curta", max_length=255, blank=True, null=True)
    imagem = models.ImageField(upload_to="perfis/", blank=True, null=True)
    logo = models.ImageField(upload_to="perfis/logos/", blank=True, null=True)
    cor_titulo = models.CharField("Cor do título", max_length=30, default="#1b1f5b", blank=True)
    ordem = models.PositiveIntegerField("Ordem", default=0)

    class Meta:
        ordering = ["ordem", "nome"]
        verbose_name = "Perfil de Formação"
        verbose_name_plural = "Perfis de Formação"

    def __str__(self):
        return self.nome


class Competencia(models.Model):
    perfil = models.ForeignKey("PerfilFormacao", on_delete=models.CASCADE, related_name="competencias")
    texto = models.CharField(max_length=255)

    def __str__(self):
        return self.texto


class AreaAtuacaoPerfil(models.Model):
    perfil = models.ForeignKey("PerfilFormacao", on_delete=models.CASCADE, related_name="areas")
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)

    def __str__(self):
        return f"{self.titulo} ({self.perfil.nome})"


# =====================================================
# VAGAS
# =====================================================

class Vaga(models.Model):
    ETAPA_CHOICES = [
        ("pendente_aprovacao", "Pendente aprovação"),
        ("publicada", "Publicada"),
        ("inscricoes_fechadas", "Inscrições fechadas"),
        ("analise_curriculos", "Análise de currículos"),
        ("entrevistas", "Entrevistas"),
        ("finalizada", "Finalizada"),
    ]
    
    TIPO_CHOICES = [
        ("estagio", "Estágio"),
        ("emprego", "Emprego"),
        ("bolsa", "Bolsa"),
    ]

    MODALIDADE_CHOICES = [
        ("presencial", "Presencial"),
        ("hibrido", "Híbrido"),
        ("remoto", "Remoto"),
    ]

    STATUS_CHOICES = [
        ("pendente", "Pendente"),
        ("aprovada", "Aprovada"),
        ("reprovada", "Reprovada"),
        ("encerrada", "Encerrada"),
    ]
    
    
    etapa = models.CharField(
        max_length=30,
        choices=ETAPA_CHOICES,
        default="pendente_aprovacao"
    )
    # Empresa agora é Usuario(tipo="empresa")
    empresa = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="vagas",
        limit_choices_to={"tipo": "empresa"},
        verbose_name="Empresa responsável",
    )

    titulo = models.CharField("Título da vaga", max_length=150)
    descricao = models.TextField("Descrição detalhada da vaga")
    requisitos = models.TextField("Requisitos", blank=True)

    curso = models.ForeignKey(
        "PerfilFormacao",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="vagas",
        verbose_name="Curso Alvo",
    )

    tipo = models.CharField("Tipo de vaga", max_length=20, choices=TIPO_CHOICES, default="estagio")
    modalidade = models.CharField("Modalidade", max_length=20, choices=MODALIDADE_CHOICES, default="presencial")

    remuneracao = models.DecimalField("Remuneração (R$)", max_digits=10, decimal_places=2, null=True, blank=True)
    cidade = models.CharField("Cidade", max_length=120, blank=True)
    bairro = models.CharField("Bairro", max_length=120, blank=True)

    status = models.CharField("Status", max_length=20, choices=STATUS_CHOICES, default="pendente")

    data_publicacao = models.DateTimeField(null=True, blank=True)
    data_inicio = models.DateField("Data de início", null=True, blank=True)
    data_fim = models.DateField("Data de término", null=True, blank=True)

    # Coordenador agora é Usuario(tipo="coordenador")
    aprovado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="vagas_aprovadas",
        limit_choices_to={"tipo": "coordenador"},
        verbose_name="Aprovado por",
    )

    class Meta:
        ordering = ["-data_publicacao"]
        verbose_name = "Vaga"
        verbose_name_plural = "Vagas"

    def __str__(self):
        # empresa.nome é o campo "nome" do Usuario
        return f"{self.titulo} — {self.empresa.nome or self.empresa.email}"

    @property
    def is_disponivel(self):
        return self.status == "aprovada"


# =====================================================
# CANDIDATURAS
# =====================================================
class Candidatura(models.Model):
    STATUS_CHOICES = [
        ("pendente", "Pendente"),
        ("analisando", "Currículo em análise"),
        ("pre_selecionado", "Pré-selecionado"),
        ("entrevista", "Entrevista agendada"),
        ("finalista", "Finalista"),
        ("aprovado", "Aprovado"),
        ("recusado", "Recusado"),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pendente"
    )

    vaga = models.ForeignKey(Vaga, on_delete=models.CASCADE, related_name="candidaturas")

    aluno = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="candidaturas",
        limit_choices_to={"tipo": "aluno"},
    )

    data_candidatura = models.DateTimeField(default=timezone.now)
    mensagem = models.TextField("Mensagem do candidato", blank=True)

    class Meta:
        unique_together = ("vaga", "aluno")
        ordering = ["-data_candidatura"]
        verbose_name = "Candidatura"
        verbose_name_plural = "Candidaturas"

    def __str__(self):
        return f"{self.aluno.nome or self.aluno.email} → {self.vaga.titulo}"




# =====================================================
# MENSAGENS DE CONTATO (formulário público)
# =====================================================
class MensagemContato(models.Model):
    nome = models.CharField("Nome", max_length=150)
    email = models.EmailField("E-mail")
    mensagem = models.TextField("Mensagem")
    data_envio = models.DateTimeField(default=timezone.now)
    resposta = models.TextField(blank=True, null=True)
    respondido = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Mensagem de Contato"
        verbose_name_plural = "Mensagens de Contato"
        ordering = ["-data_envio"]

    def __str__(self):
        return f"{self.nome} — {self.email}"


# =====================================================
# CONFIGURAÇÃO DO SITE
# =====================================================
class SiteConfig(models.Model):
    titulo_banner = models.CharField(max_length=200, default="Da ideia à prática, do campus à carreira.")
    subtitulo_banner = models.CharField(max_length=255, default="Aprender, se conectar e crescer: seu futuro começa aqui.")
    imagem_banner = models.ImageField(upload_to="home/", blank=True, null=True)
    
    nome_site = models.CharField("Nome do site", max_length=100, default="LinkIF")
    descricao_curta = models.TextField(
        default="Conectando talentos técnicos do IFRN às melhores oportunidades profissionais."
    )
    email_contato = models.EmailField(default="contato@ifrn.edu.br")
    telefone = models.CharField(max_length=50, default="(84) 98888-8888")
    endereco = models.CharField(max_length=255, default="Av. Potengi, São Paulo do Potengi - RN")
    instagram = models.URLField(blank=True, null=True)
    mapa_embed = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to="site/logo/", blank=True, null=True)

    class Meta:
        verbose_name = "Configuração do Site"
        verbose_name_plural = "Configurações do Site"

    def __str__(self):
        return self.nome_site

    @property
    def get_logo_url(self):
        if self.logo and hasattr(self.logo, "url"):
            return self.logo.url
        return "/static/assets/img/logo.svg"

