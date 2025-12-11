from django.db import models
from django.contrib.auth.models import AbstractUser, Permission


class Usuario(AbstractUser):
    TIPO_CHOICES = [
        ("aluno", "Aluno"),
        ("empresa", "Empresa"),
        ("coordenador", "Coordenação"),
    ]

    # ================================
    # CAMPOS DO USUÁRIO
    # ================================
    email = models.EmailField("E-mail", unique=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)

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
    status_aprovacao = models.CharField(
        max_length=20,
        choices=[
            ("pendente", "Pendente"),
            ("aprovado", "Aprovado"),
            ("reprovado", "Reprovado"),
        ],
        default="pendente"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    # ================================
    # PERMISSÕES DO SISTEMA
    # ================================
    class Meta:
        permissions = [
            ("acesso_aluno", "Pode acessar a área do aluno"),
            ("acesso_empresa", "Pode acessar a área da empresa"),
            ("acesso_coordenacao", "Pode acessar a área da coordenação"),

            ("can_candidatar", "Pode se candidatar a vagas"),
            ("can_explorar_alunos", "Pode visualizar perfis de alunos"),
            ("can_post_vaga", "Pode cadastrar vaga"),

            ("aluno_aprovado", "Aluno aprovado pela coordenação"),
            ("empresa_aprovada", "Empresa aprovada pela coordenação"),
        ]

    # ================================
    # PERMISSÕES AUTOMÁTICAS
    # ================================
    def aplicar_permissoes_por_tipo(self):
        """Define permissões automáticas conforme tipo + aprovação."""

        self.user_permissions.clear()
        codigos = []

        # ----------------- ALUNO -----------------
        if self.tipo == "aluno":
            codigos.append("acesso_aluno")
            codigos.append("can_candidatar")

            if self.is_approved:
                codigos.append("aluno_aprovado")

        # ----------------- EMPRESA -----------------
        elif self.tipo == "empresa":
            codigos.append("acesso_empresa")
            codigos.append("can_explorar_alunos")

            if self.is_approved:
                codigos.append("can_post_vaga")
                codigos.append("empresa_aprovada")

        # ----------------- COORDENAÇÃO -----------------
        elif self.tipo == "coordenador":
            codigos.append("acesso_coordenacao")
            codigos.append("can_post_vaga")
            codigos.append("can_explorar_alunos")

        # aplica permissões
        for codename in codigos:
            try:
                perm = Permission.objects.get(codename=codename)
                self.user_permissions.add(perm)
            except Permission.DoesNotExist:
                pass

    # ================================
    # SAVE COM CORREÇÃO DO SUPERUSER
    # ================================
    def save(self, *args, **kwargs):

        # SE FOR SUPERUSER → vira coordenação aprovada automaticamente
        if self.is_superuser:
            self.tipo = "coordenador"
            self.is_approved = True
            self.status_aprovacao = "aprovado"

        super().save(*args, **kwargs)

        # depois de salvar, aplica permissões
        self.aplicar_permissoes_por_tipo()

    def __str__(self):
        return f"{self.username} — {self.email} ({self.tipo})"
