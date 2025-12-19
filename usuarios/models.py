from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Permission
from django.utils.translation import gettext_lazy as _

class UsuarioManager(BaseUserManager):
    '''
    Usuário admin do Django usando email no lugar de username
    '''
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('O campo email é obrigatório'))
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_approved', True)
        extra_fields.setdefault('tipo', 'coordenador')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        
        return self.create_user(email, password, **extra_fields)

class Usuario(AbstractUser):
    TIPO_CHOICES = [
        ("aluno", "Aluno"),
        ("empresa", "Empresa"),
        ("coordenador", "Coordenação"),
    ]

    # ================================
    # CAMPOS DO USUÁRIO
    # ================================
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
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
    objects = UsuarioManager()
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
        """
        Garante que username seja único, mas não obrigatório
        """
        if not self.username:
            base_username = self.email.split('@')[0]
            username = base_username
            counter = 1
            
            while Usuario.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            
            self.username = username

        # sincroniza status -> boolean
        self.is_approved = self.status_aprovacao == "aprovado"

        if self.is_superuser:
            self.tipo = "coordenador"
            self.status_aprovacao = "aprovado"
            self.is_approved = True

        super().save(*args, **kwargs)

        self.aplicar_permissoes_por_tipo()

    def __str__(self):
        return f"{self.username} — {self.email} ({self.tipo})"
