from django.db import models
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
    TIPO_CHOICES = [
        ("aluno", "Aluno"),
        ("empresa", "Empresa"),
        ("coordenador", "Coordenação"),
    ]

    email = models.EmailField("E-mail", unique=True)

    # tipo de usuário
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)

    # dados gerais
    nome = models.CharField(max_length=120, blank=True, null=True)

    # aluno
    curso = models.CharField(max_length=100, blank=True, null=True)
    foto = models.ImageField(upload_to="foto-perfil/", blank=True, null=True)
    curriculo = models.FileField(upload_to="curriculos/", blank=True, null=True)
    portfolio = models.URLField(blank=True, null=True)
    resumo = models.TextField(blank=True, null=True)

    # empresa
    cnpj = models.CharField(max_length=18, blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    setor = models.CharField(max_length=120, blank=True, null=True)

    # controle
    is_approved = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]  # necessário pro createsuperuser

    def __str__(self):
        return f"{self.username} — {self.email} ({self.tipo})"
