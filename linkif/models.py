from django.db import models
from django.conf import settings
from django.utils import timezone
from usuarios.models import Empresa, Coordenador


# =====================================================
# ÁREA DE ATUAÇÃO
# =====================================================
class AreaAtuacao(models.Model):
    nome = models.CharField("Nome da área", max_length=100, unique=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Área de Atuação"
        verbose_name_plural = "Áreas de Atuação"
        ordering = ["nome"]


# =====================================================
# VAGAS
# =====================================================
class Vaga(models.Model):
    TIPO_CHOICES = [
        ('estagio', 'Estágio'),
        ('emprego', 'Emprego'),
        ('bolsa', 'Bolsa'),
    ]

    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('aprovada', 'Aprovada'),
        ('reprovada', 'Reprovada'),
        ('encerrada', 'Encerrada'),
    ]

    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name='vagas',
        verbose_name="Empresa responsável"
    )
    titulo = models.CharField("Título da vaga", max_length=150)
    descricao = models.TextField("Descrição detalhada da vaga")
    requisitos = models.TextField("Requisitos", blank=True)
    area = models.ForeignKey(
        AreaAtuacao,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Área de atuação"
    )
    tipo = models.CharField("Tipo de vaga", max_length=20, choices=TIPO_CHOICES, default='estagio')
    remuneracao = models.DecimalField("Remuneração (R$)", max_digits=10, decimal_places=2, null=True, blank=True)
    cidade = models.CharField("Cidade", max_length=120, blank=True)
    estado = models.CharField("Estado", max_length=60, blank=True)
    bairro = models.CharField("Bairro", max_length=120, blank=True)
    status = models.CharField("Status", max_length=20, choices=STATUS_CHOICES, default='pendente')
    data_publicacao = models.DateTimeField("Data de publicação", default=timezone.now)
    data_inicio = models.DateField("Data de início", null=True, blank=True)
    data_fim = models.DateField("Data de término", null=True, blank=True)
    aprovado_por = models.ForeignKey(
        Coordenador,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Aprovado por"
    )

    class Meta:
        ordering = ['-data_publicacao']
        verbose_name = "Vaga"
        verbose_name_plural = "Vagas"

    def __str__(self):
        return f"{self.titulo} — {self.empresa.nome_empresa}"

    @property
    def is_disponivel(self):
        return self.status == "aprovada"
# =====================================================
# CANDIDATURAS
# =====================================================

class Candidatura(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('em_analise', 'Em análise'),
        ('aprovado', 'Aprovado'),
        ('recusado', 'Recusado'),
    ]

    vaga = models.ForeignKey(Vaga, on_delete=models.CASCADE, related_name='candidaturas')
    aluno = models.ForeignKey('usuarios.Aluno', on_delete=models.CASCADE, related_name='candidaturas')
    data_candidatura = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    mensagem = models.TextField("Mensagem do candidato", blank=True)

    class Meta:
        unique_together = ('vaga', 'aluno')
        ordering = ['-data_candidatura']
        verbose_name = "Candidatura"
        verbose_name_plural = "Candidaturas"

    def __str__(self):
        return f"{self.aluno.usuario.get_full_name() or self.aluno.usuario.username} → {self.vaga.titulo}"


# =====================================================
# NOTIFICAÇÕES E MENSAGENS
# =====================================================




class Mensagem(models.Model):
    remetente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mensagens_enviadas')
    destinatario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mensagens_recebidas')
    conteudo = models.TextField()
    data_envio = models.DateTimeField(default=timezone.now)
    lida = models.BooleanField(default=False)

    class Meta:
        ordering = ['-data_envio']
        verbose_name = "Mensagem"
        verbose_name_plural = "Mensagens"

    def __str__(self):
        return f"{self.remetente.username} → {self.destinatario.username}"


# =====================================================
# CONFIGURAÇÕES DO SITE (rodapé, contato, etc.)
# =====================================================

class SiteConfig(models.Model):
    nome_site = models.CharField("Nome do site", max_length=100, default="LinkIF")
    descricao_curta = models.TextField(
        "Descrição curta",
        default="Conectando talentos técnicos do IFRN às melhores oportunidades profissionais.",
    )
    email_contato = models.EmailField("E-mail de contato", default="contato@ifrn.edu.br")
    telefone = models.CharField("Telefone", max_length=50, default="(84) 98888-8888")
    endereco = models.CharField(
        "Endereço", max_length=255, default="Av. Potengi, São Paulo do Potengi - RN, 59460-000"
    )
    instagram = models.URLField("Instagram", blank=True, null=True)
    mapa_embed = models.TextField(
        "Mapa (iframe do Google Maps)", blank=True, null=True, help_text="Cole aqui o código embed do Google Maps."
    )

    class Meta:
        verbose_name = "Configuração do Site"
        verbose_name_plural = "Configurações do Site"

    def __str__(self):
        return self.nome_site

    @property
    def get_logo_url(self):
        if self.logo and hasattr(self.logo, 'url'):
            return self.logo.url
        return "/static/assets/img/logo.png"  # fallback


# =====================================================
# CONTEÚDO DA HOME
# =====================================================

class HomeContent(models.Model):
    titulo_banner = models.CharField("Título do Banner", max_length=200, default="Da ideia à prática, do campus à carreira.")
    subtitulo_banner = models.CharField("Subtítulo do Banner", max_length=255, default="Aprender, se conectar e crescer: seu futuro começa aqui.")
    imagem_banner = models.ImageField(upload_to="home/", blank=True, null=True)

    titulo_sobre = models.CharField("Título da seção Sobre", max_length=100, default="O que é o LinkIF?")
    texto_sobre = models.TextField(
        "Texto da seção Sobre",
        default="O LinkIF é uma plataforma do IFRN – Campus São Paulo do Potengi que conecta estudantes, ex-alunos e empresas.",
    )

    card1_titulo = models.CharField(max_length=100, default="Plataforma Integrada")
    card1_texto = models.TextField(default="Um ambiente digital criado para centralizar estágios e oportunidades profissionais no Potengi.")
    card1_icon = models.ImageField(upload_to="home/icons/", blank=True, null=True)

    card2_titulo = models.CharField(max_length=100, default="Conexão Estratégica")
    card2_texto = models.TextField(default="Coloca em diálogo estudantes e empresas, aproximando o IFRN do mercado de trabalho.")
    card2_icon = models.ImageField(upload_to="home/icons/", blank=True, null=True)

    card3_titulo = models.CharField(max_length=100, default="Porta de entrada")
    card3_texto = models.TextField(default="Mais que um sistema, o LinkIF é o caminho para transformar formação técnica em experiência real.")
    card3_icon = models.ImageField(upload_to="home/icons/", blank=True, null=True)

    titulo_estudantes = models.CharField(max_length=100, default="Para Estudantes")
    texto_estudantes = models.TextField(default="Mostre suas habilidades e encontre oportunidades que combinam com você.")
    imagem_estudantes = models.ImageField(upload_to="home/", blank=True, null=True)

    titulo_empresas = models.CharField(max_length=100, default="Para Empresas")
    texto_empresas = models.TextField(default="Encontre os talentos que fazem a diferença e fortaleça sua equipe com jovens qualificados do IFRN.")
    imagem_empresas = models.ImageField(upload_to="home/", blank=True, null=True)
    
        # --- Seção "Para Estudantes" ---
    estudante_card1_titulo = models.CharField(max_length=100, default="Monte seu Perfil")
    estudante_card1_texto = models.TextField(default="Crie seu perfil profissional e destaque suas habilidades para empresas e oportunidades de estágio.")

    estudante_card2_titulo = models.CharField(max_length=100, default="Conecte-se às Empresas")
    estudante_card2_texto = models.TextField(default="Entre em contato direto com empresas da região e participe de processos seletivos simplificados.")

    estudante_card3_titulo = models.CharField(max_length=100, default="Encontre Vagas")
    estudante_card3_texto = models.TextField(default="Acesse vagas de estágio, emprego e projetos de pesquisa disponíveis no LinkIF.")

    estudante_card4_titulo = models.CharField(max_length=100, default="Cresça com o IFRN")
    estudante_card4_texto = models.TextField(default="Amplie sua experiência e fortaleça seu currículo através de oportunidades reais.")

    estudante_cta_titulo = models.CharField(max_length=150, default="Pronto para dar o próximo passo?")
    estudante_cta_texto = models.TextField(default="Explore as oportunidades disponíveis e inicie sua trajetória profissional.")

    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Conteúdo da Página Inicial"
        verbose_name_plural = "Conteúdos da Página Inicial"

    def __str__(self):
        return "Conteúdo principal da Home"
# =====================================================
# PERFIS DE FORMAÇÃO (DINÂMICO)
# =====================================================

class PerfilFormacao(models.Model):
    nome = models.CharField("Nome do Curso", max_length=120, unique=True)
    descricao = models.TextField("Descrição", blank=True)
    imagem = models.ImageField(upload_to="perfis/", blank=True, null=True)
    logo = models.ImageField(upload_to="perfis/logos/", blank=True, null=True)
    cor_titulo = models.CharField(
        "Cor do título (opcional, hex ou nome)", max_length=30, blank=True, default="#1b1f5b"
    )
    ordem = models.PositiveIntegerField("Ordem de exibição", default=0)

    class Meta:
        ordering = ["ordem", "nome"]
        verbose_name = "Perfil de Formação"
        verbose_name_plural = "Perfis de Formação"

    def __str__(self):
        return self.nome
class Competencia(models.Model):
    perfil = models.ForeignKey('PerfilFormacao', on_delete=models.CASCADE, related_name='competencias')
    texto = models.CharField(max_length=255)

    def __str__(self):
        return self.texto


class AreaAtuacaoPerfil(models.Model):
    perfil = models.ForeignKey('PerfilFormacao', on_delete=models.CASCADE, related_name='areas')
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)

    def __str__(self):
        return f"{self.titulo} ({self.perfil.nome})"
    
class MensagemContato(models.Model):
    nome = models.CharField("Nome", max_length=150)
    email = models.EmailField("E-mail")
    mensagem = models.TextField("Mensagem")
    data_envio = models.DateTimeField("Data de envio", default=timezone.now)
    respondido = models.BooleanField("Respondido?", default=False)

    class Meta:
        verbose_name = "Mensagem de Contato"
        verbose_name_plural = "Mensagens de Contato"
        ordering = ['-data_envio']

    def __str__(self):
        return f"{self.nome} — {self.email}"
    
# =====================================================
# FEATURES (Estudantes e Empresas)
# =====================================================
class Feature(models.Model):
    TIPO_CHOICES = [
        ('estudante', 'Para Estudantes'),
        ('empresa', 'Para Empresas'),
    ]

    tipo = models.CharField(
        "Tipo de público",
        max_length=20,
        choices=TIPO_CHOICES,
        default='estudante'
    )
    icone = models.CharField(
        "Ícone Bootstrap",
        max_length=50,
        help_text="Exemplo: bi-person-circle, bi-building, bi-rocket-takeoff"
    )
    titulo = models.CharField("Título", max_length=120)
    descricao = models.TextField("Descrição")
    ordem = models.PositiveIntegerField("Ordem de exibição", default=0)

    class Meta:
        ordering = ['tipo', 'ordem']
        verbose_name = "Feature"
        verbose_name_plural = "Features (Estudantes e Empresas)"

    def __str__(self):
        return f"{self.titulo} — {self.get_tipo_display()}"