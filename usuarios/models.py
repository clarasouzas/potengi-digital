from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings



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
    foto = models.ImageField(upload_to="fotos_perfil/", null=True, blank=True)

    def __str__(self):
        return self.usuario.get_full_name() or self.usuario.email

    class Meta:
        verbose_name = "Aluno"
        verbose_name_plural = "Alunos"


# =====================================================
# PERFIL DA EMPRESA
# =====================================================

class Empresa(models.Model):
    nome_empresa = models.CharField(
        max_length=100,
        verbose_name="Nome da Empresa",
        help_text="Nome público da empresa (ex: Tech Solutions)"
    )
    razao_social = models.CharField(
        max_length=150,
        verbose_name="Razão Social",
        help_text="Nome jurídico completo (ex: Tech Solutions LTDA)"
    )
    cnpj = models.CharField(
        max_length=18,
        unique=True,
        verbose_name="CNPJ",
        help_text="Digite apenas números ou use o formato 00.000.000/0000-00"
    )
    telefone = models.CharField(
        max_length=20,
        verbose_name="Telefone de Contato",
        help_text="Inclua o DDD (ex: (84) 99999-9999)"
    )
    email = models.EmailField(
        unique=True,
        verbose_name="Email Corporativo",
        help_text="Email institucional usado para login"
    )
    site = models.URLField(
        blank=True,
        null=True,
        verbose_name="Site da Empresa",
        help_text="Opcional — ex: https://empresa.com.br"
    )
    descricao = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descrição da Empresa",
        help_text="Fale brevemente sobre a atuação, missão ou área de interesse"
    )

    # Endereço
    logradouro = models.CharField(
        max_length=100,
        verbose_name="Logradouro",
        help_text="Rua, avenida ou local onde a empresa está localizada"
    )
    bairro = models.CharField(
        blank=True,
        max_length=100,
        verbose_name="Bairro"
    )
    cidade = models.CharField(
        max_length=100,
        verbose_name="Cidade"
    )
    estado = models.CharField(
        max_length=2,
        verbose_name="Estado (UF)",
        help_text="Use a sigla — ex: RN"
    )
    cep = models.CharField(
        blank=True,
        max_length=10,
        verbose_name="CEP",
        help_text="Ex: 59000-000"
    )

    # Informações adicionais
    setor = models.CharField(
        max_length=80,
        blank=True,
        null=True,
        verbose_name="Setor de Atuação",
        help_text="Ex: Tecnologia da Informação, Educação, Comércio..."
    )
    tamanho_empresa = models.CharField(
        max_length=20,
        choices=[
            ('pequena', 'Pequena'),
            ('media', 'Média'),
            ('grande', 'Grande')
        ],
        blank=True,
        null=True,
        verbose_name="Porte da Empresa"
    )
    logo = models.ImageField(
        upload_to="empresas/logos/",
        blank=True,
        null=True,
        verbose_name="Logo da Empresa",
        help_text="Imagem em formato PNG ou JPG"
    )

    data_cadastro = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Cadastro"
    )

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        ordering = ["-data_cadastro"]

    def __str__(self):
        return self.nome_empresa



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

class Notificacao(models.Model):
    tipo = models.CharField(max_length=80)
    mensagem = models.TextField()
    usuario_destino = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notificacoes')
    data_envio = models.DateTimeField(default=timezone.now)
    lida = models.BooleanField(default=False)

    class Meta:
        ordering = ['-data_envio']
        verbose_name = "Notificação"
        verbose_name_plural = "Notificações"

    def __str__(self):
        return f"{self.tipo} → {self.usuario_destino.username}"
