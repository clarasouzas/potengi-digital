from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class Usuario(AbstractUser):
    TIPO_CHOICES = [
        ("aluno", "Aluno"),
        ("empresa", "Empresa"),
        ("coordenador", "Coordenação"),
    ]

    email = models.EmailField("E-mail", unique=True)
    tipo = models.CharField("Tipo de usuário", max_length=20, choices=TIPO_CHOICES)
    is_approved = models.BooleanField("Aprovado pela coordenação", default=False)

    # remover username como campo obrigatório
    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # somente email e senha

    def __str__(self):
        return self.email

class Aluno(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name="aluno")
    nome = models.CharField(max_length=100, blank=True, null=True) 
    curso = models.CharField(max_length=100)
    foto = models.ImageField(upload_to="foto-aluno/", blank=True, null=True)
    curriculo = models.FileField(upload_to="curriculos/", blank=True, null=True)
    portfolio = models.URLField(blank=True, null=True)
    criado_em = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nome
class Empresa(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name="empresa")

    nome_empresa = models.CharField(max_length=150,blank=True, null=True)
    cnpj = models.CharField(max_length=18, unique=True)
    telefone = models.CharField(max_length=20)
    cidade = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome_empresa
class Coordenador(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name="coordenador")
    nome = models.CharField(max_length=100,blank=True, null=True)
    setor = models.CharField(max_length=100)

    def __str__(self):
        return self.nome
