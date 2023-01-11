from django.db import models
from django.urls import reverse_lazy, reverse
from django.core.validators import RegexValidator
# Create your models here.


class Users(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=255)

    class Meta:
        db_table = 'auth_user'
        managed = False


class Cursos(models.Model):
    id = models.IntegerField(primary_key=True)
    id_eixos = models.IntegerField()
    tipo = models.IntegerField()
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome

    class Meta:
        db_table = 'qualificacoes'


class Solicitacao(models.Model):
    id = models.IntegerField(primary_key=True)
    eixo = models.CharField(max_length=255)
    curso = models.CharField(max_length=255)
    modalidade = models.CharField(max_length=255)
    tipo = models.CharField(max_length=255)
    justificativa = models.CharField(max_length=255)

    class Meta:
        db_table = 'appprojeto1_solicitacao'


class Metas_escolas(models.Model):
    id = models.IntegerField(primary_key=True)
    escola = models.CharField(max_length=255)
    tipo = models.IntegerField()
    email = models.EmailField(max_length=255)
    telefone = models.CharField(max_length=16)

    def __str__(self):
        return self.escola

    class Meta:
        db_table = 'escolas'
        ordering = ('escola',)


class Eixos(models.Model):
    id = models.IntegerField(primary_key=True)
    eixo_id = models.IntegerField()
    escola = models.ForeignKey(Metas_escolas, on_delete=models.CASCADE)
    nome = models.CharField(max_length=255)
    status = models.CharField(max_length=255)

    def __str__(self):
        return self.nome

    class Meta:
        db_table = 'eixos'


class Metas_tipo(models.Model):
    id = models.IntegerField(primary_key=True)
    tipo = models.CharField(max_length=255)

    def __str__(self):
        return self.tipo

    class Meta:
        db_table = 'tipo_curso'


class Metas_modalidade(models.Model):
    id = models.IntegerField(primary_key=True)
    modalidade = models.CharField(max_length=255)

    def __str__(self):
        return self.modalidade

    class Meta:
        db_table = 'modalidade'


class Metas_trimestre(models.Model):
    id = models.IntegerField(primary_key=True)
    trimestre = models.CharField(max_length=255)

    def __str__(self):
        return self.trimestre

    class Meta:
        db_table = 'trimestre'


class Metas_descricoes(models.Model):
    id = models.IntegerField(primary_key=True)
    descricao = models.CharField(max_length=255)

    def __str__(self):
        return self.descricao

    class Meta:
        db_table = 'descricao'


class Metas_sinteticas(models.Model):
    id = models.IntegerField(primary_key=True)
    diretoria = models.CharField(max_length=255)
    escola = models.ForeignKey(Metas_escolas, on_delete=models.CASCADE)
    ano = models.IntegerField()
    modalidade = models.ForeignKey(Metas_modalidade, on_delete=models.CASCADE)
    descricao = models.ForeignKey(Metas_descricoes, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Metas_tipo, on_delete=models.CASCADE)
    ch_ofertada = models.IntegerField()
    vagas = models.IntegerField()
    repasse = models.FloatField()
    valor_unitario = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        db_table = 'Metas_sinteticas_efg'


class Rubrica(models.Model):
    id = models.IntegerField(primary_key=True)
    rubrica = models.CharField(max_length=255)

    class Meta:
        db_table = 'rubrica'


class Item_apoiado(models.Model):
    id = models.IntegerField(primary_key=True)
    id_rubrica = models.IntegerField()
    item_apoiado = models.CharField(max_length=255)

    class Meta:
        db_table = 'item_apoiado'


class Unidades(models.Model):
    id = models.IntegerField(primary_key=True)
    und = models.CharField(max_length=255)

    class Meta:
        db_table = 'unidade'


class Curso_escola(models.Model):
    id = models.IntegerField(primary_key=True)
    escola_id = models.IntegerField()
    curso_id = models.IntegerField()
    status = models.CharField(max_length=255)

    class Meta:
        db_table = 'curso_escola'
        

class Cadastrar_curso(models.Model):
    id = models.IntegerField(primary_key=True)
    escola = models.ForeignKey(Metas_escolas, on_delete=models.CASCADE)
    tipo = models.ForeignKey(Metas_tipo, on_delete=models.CASCADE)
    eixos = models.ForeignKey(Eixos, on_delete=models.CASCADE)
    curso = models.CharField(max_length=255)
    modalidade = models.ForeignKey(Metas_modalidade, on_delete=models.CASCADE)
    status = models.CharField(max_length=255)
    escolaridade = models.CharField(max_length=255)
    idade_min = models.IntegerField()
    carga_horaria = models.IntegerField()
    siga_id = models.IntegerField()

    def __str__(self):
        return self.curso

    class Meta:
        db_table = 'cursos'
        ordering = ('curso',)


class Orcamento_plano_trabalho(models.Model):
    id = models.IntegerField(primary_key=True)
    tipo = models.CharField(max_length=255)
    rubrica = models.ForeignKey(Rubrica, on_delete=models.CASCADE)
    item_apoiado = models.ForeignKey(Item_apoiado, on_delete=models.CASCADE)
    und = models.CharField(max_length=255)
    qtd_global = models.DecimalField(max_digits=15, decimal_places=2)
    valor_medio_unitario = models.DecimalField(max_digits=15, decimal_places=2)
    valor_global = models.DecimalField(max_digits=15, decimal_places=2)
    custeio = models.DecimalField(max_digits=15, decimal_places=2)
    capital = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        db_table = 'planejamento_trabalho'


class Udepi_municipio(models.Model):
    id = models.IntegerField(primary_key=True)
    escola = models.ForeignKey(Metas_escolas, on_delete=models.CASCADE)
    municipio = models.CharField(max_length=255)

    def __str__(self):
        return self.municipio

    class Meta:
        db_table = 'udepi_municipio'


class Edital(models.Model):
    id = models.IntegerField(primary_key=True)
    num_edital = models.IntegerField()
    ano = models.IntegerField()
    dt_ini_edit = models.DateField(null=True, blank=True)
    dt_fim_edit = models.DateField(null=True, blank=True)
    dt_ini_insc = models.DateField(null=True, blank=True)
    dt_fim_insc = models.DateField(null=True, blank=True)
    escola = models.ForeignKey(Metas_escolas, on_delete=models.CASCADE)
    status = models.CharField(max_length=255)
    pdf = models.CharField(max_length=255)
    motivo = models.CharField(max_length=255)

    def __str__(self):
        return self.num_edital

    class Meta:

        db_table = 'edital_ensino'
        managed = True


class Metas_efg(models.Model):
    SITUACAO = (
        (0, 'Aguardando Análise'),
        (1, 'Reprovado',),
        (2, 'Em Análise'),
        (3, 'Aprovado',),
    )

    DIRETORIAS = (
        ('DAC', 'DAC'),
        ('DDA', 'DDA'),
        ('DE', 'DE'),
    )

    SEMESTRES = (
        (1, '1º SEMESTRE'),
        (2, '2º SEMESTRE'),
    )

    TURNOS = (
        ('MATUTINO', 'MATUTINO'),
        ('VESPERTINO', 'VESPERTINO'),
        ('NOTURNO', 'NOTURNO'),
    )

    id = models.IntegerField(primary_key=True)
    diretoria = models.CharField(max_length=255, choices=DIRETORIAS)
    escola = models.ForeignKey(Metas_escolas, on_delete=models.CASCADE)
    tipo_curso = models.ForeignKey(Metas_tipo, on_delete=models.CASCADE)
    curso = models.ForeignKey(Cadastrar_curso, on_delete=models.CASCADE)
    turno = models.CharField(max_length=255, choices=TURNOS)
    ano = models.IntegerField()
    modalidade = models.ForeignKey(Metas_modalidade, on_delete=models.CASCADE)
    trimestre = models.IntegerField(choices=SEMESTRES)
    vagas_totais = models.IntegerField()
    carga_horaria = models.IntegerField()
    carga_horaria_total = models.IntegerField()
    previsao_inicio = models.DateField()
    previsao_fim = models.DateField()
    dias_semana = models.CharField(max_length=255)
    previsao_abertura_edital = models.DateField(null=True, blank=True)
    previsao_fechamento_edital = models.DateField(null=True, blank=True)
    data_registro = models.DateField(null=True, blank=True)
    eixo = models.ForeignKey(Eixos, on_delete=models.CASCADE)
    udepi = models.ForeignKey(Udepi_municipio, on_delete=models.CASCADE)
    situacao = models.IntegerField(
        default=0, choices=SITUACAO, null=True, blank=True)
    jus_reprovacao = models.TextField(default=None, null=True, blank=True)
    num_edital = models.ForeignKey(
        Edital, on_delete=models.CASCADE, default=None, null=True, blank=True)

    def get_absolute_url(self):
        return reverse_lazy('AprovarCursosView')

    def __str__(self):
        return self.curso

    class Meta:
        managed = True
        db_table = 'Turmas_planejado_orcado'


class User_permission(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    permission = models.CharField(max_length=255)
    escola = models.ForeignKey(Metas_escolas, on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_permission'

class Users_ids(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    user_selecao_id =  models.IntegerField()
    user_siga_id = models.IntegerField()

    class Meta:
        db_table = 'users_siga_selecao'