from django.db import models
from django.contrib.auth.models import AbstractUser, Permission


class Usuario(AbstractUser):
    TIPO_CHOICES = [
        ("aluno", "Aluno"),
        ("empresa", "Empresa"),
        ("coordenador", "Coordenação"),
    ]

    # dados básicos
    email = models.EmailField("E-mail", unique=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
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
    REQUIRED_FIELDS = ["username"]

    class Meta:
        permissions = [
            # acesso geral por tipo
            ("acesso_aluno", "Pode acessar a área do aluno"),
            ("acesso_empresa", "Pode acessar a área da empresa"),
            ("acesso_coordenacao", "Pode acessar a área da coordenação"),

            # permissões especiais
            ("can_candidatar", "Pode se candidatar a vagas"),
            ("can_explorar_alunos", "Pode visualizar perfis de alunos"),

            # aprovado
            ("aluno_aprovado", "Aluno aprovado pela coordenação"),
            ("empresa_aprovada", "Empresa aprovada pela coordenação"),
        ]

    # -------------------------------------
    # APLICAÇÃO AUTOMÁTICA DE PERMISSÕES
    # -------------------------------------
    def aplicar_permissoes_por_tipo(self):
        """Define permissões automáticas conforme tipo + aprovação."""

        self.user_permissions.clear()
        codigos = []

        # aluno
        if self.tipo == "aluno":
            codigos.append("acesso_aluno")
            codigos.append("can_candidatar")
            if self.is_approved:
                codigos.append("aluno_aprovado")

        # empresa
        elif self.tipo == "empresa":
            codigos.append("acesso_empresa")
            if self.is_approved:
                codigos.append("empresa_aprovada")

            # Empresa pode explorar perfis?
            codigos.append("can_explorar_alunos")

        # coordenação
        elif self.tipo == "coordenador":
            codigos.append("acesso_coordenacao")
            codigos.append("can_explorar_alunos")

        # aplica permissões existentes
        for codename in codigos:
            try:
                perm = Permission.objects.get(codename=codename)
                self.user_permissions.add(perm)
            except Permission.DoesNotExist:
                pass

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.aplicar_permissoes_por_tipo()

    def __str__(self):
        return f"{self.username} — {self.email} ({self.tipo})"
