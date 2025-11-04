from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


# =====================================================
# USUÁRIO BASE (AbstractUser com e-mail e tipo)
# =====================================================
class Usuario(AbstractUser):
    TIPO_CHOICES = [
        ("aluno", "Aluno"),
        ("empresa", "Empresa"),
        ("coordenador", "Coordenação"),
    ]

    email = models.EmailField("E-mail", unique=True)
    tipo = models.CharField("Tipo de usuário", max_length=20, choices=TIPO_CHOICES)
    is_approved = models.BooleanField("Aprovado pela coordenação", default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return f"{self.email} ({self.get_tipo_display()})"

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"


# =====================================================
# PERFIL DO ALUNO
# =====================================================
class Aluno(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name="aluno")
    curso = models.CharField("Curso", max_length=100, blank=True)
    curriculo = models.FileField(upload_to="curriculos/", blank=True, null=True)
    portfolio = models.URLField("Portfólio (opcional)", blank=True, null=True)
    criado_em = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.usuario.get_full_name() or self.usuario.email

    class Meta:
        verbose_name = "Aluno"
        verbose_name_plural = "Alunos"


# =====================================================
# PERFIL DA EMPRESA
# =====================================================
class Empresa(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name="empresa")
    nome_fantasia = models.CharField("Nome Fantasia", max_length=150)
    cnpj = models.CharField("CNPJ", max_length=18, unique=True)
    area_atuacao = models.CharField("Área de Atuação", max_length=150, blank=True)
    endereco = models.CharField("Endereço", max_length=255, blank=True)
    telefone = models.CharField("Telefone", max_length=50, blank=True)
    site = models.URLField("Site", blank=True, null=True)
    criado_em = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nome_fantasia

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"


# =====================================================
# PERFIL DA COORDENAÇÃO
# =====================================================
class Coordenador(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name="coordenador")
    setor = models.CharField("Setor ou Departamento", max_length=100, blank=True)
    criado_em = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.usuario.get_full_name() or self.usuario.email

    class Meta:
        verbose_name = "Coordenador"
        verbose_name_plural = "Coordenadores"
