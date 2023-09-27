from django.db import models
from django.urls import reverse_lazy
from django.contrib.auth.models import User


class Cursos(models.Model):
    id = models.AutoField(primary_key=True)
    id_eixos = models.IntegerField()
    tipo = models.IntegerField()
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome

    class Meta:
        managed = True
        db_table = 'qualificacoes'


class Solicitacao(models.Model):
    id = models.AutoField(primary_key=True)
    eixo = models.CharField(max_length=255)
    curso = models.CharField(max_length=255)
    modalidade = models.CharField(max_length=255)
    tipo = models.CharField(max_length=255)
    justificativa = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'appprojeto1_solicitacao'


class Metas_escolas(models.Model):

    TIPO = (
        (0, 'EFG'),
        (1, 'COTEC'),
        (2, 'UDEPI'),
        (3, 'CVT'),
        (4, 'Salas de Extensão'),
    )

    id = models.AutoField(primary_key=True)
    escola = models.CharField(max_length=255, null=False, blank=False)
    tipo = models.IntegerField(null=False, blank=False, choices=TIPO)
    email = models.EmailField(max_length=255, null=True, blank=True)
    telefone = models.CharField(max_length=16, null=True, blank=True)
    selecao_id = models.IntegerField(null=True, default=None)

    def __str__(self):
        return self.escola

    class Meta:
        managed = True
        db_table = 'escolas'
        ordering = ('escola',)


class Eixos(models.Model):
    id = models.AutoField(primary_key=True)
    eixo_id = models.IntegerField()
    escola = models.ForeignKey(Metas_escolas, on_delete=models.CASCADE)
    nome = models.CharField(max_length=255)
    status = models.CharField(max_length=255)

    def __str__(self):
        return self.nome

    class Meta:
        managed = True
        db_table = 'eixos'


class Metas_tipo(models.Model):

    id = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=255)

    def __str__(self):
        return self.tipo

    class Meta:
        managed = True
        db_table = 'tipo_curso'


class Metas_modalidade(models.Model):
    id = models.AutoField(primary_key=True)
    modalidade = models.CharField(max_length=255)

    def __str__(self):
        return self.modalidade

    class Meta:
        managed = True
        db_table = 'modalidade'


class Metas_trimestre(models.Model):
    id = models.AutoField(primary_key=True)
    trimestre = models.CharField(max_length=255)

    def __str__(self):
        return self.trimestre

    class Meta:
        managed = True
        db_table = 'trimestre'


class Metas_descricoes(models.Model):
    id = models.AutoField(primary_key=True)
    descricao = models.CharField(max_length=255)

    def __str__(self):
        return self.descricao

    class Meta:
        managed = True
        db_table = 'descricao'


class Metas_sinteticas(models.Model):
    id = models.AutoField(primary_key=True)
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
        managed = True
        db_table = 'Metas_sinteticas_efg'


class Rubrica(models.Model):
    id = models.AutoField(primary_key=True)
    rubrica = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'rubrica'


class Item_apoiado(models.Model):
    id = models.AutoField(primary_key=True)
    id_rubrica = models.IntegerField()
    item_apoiado = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'item_apoiado'


class Unidades(models.Model):
    id = models.AutoField(primary_key=True)
    und = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'unidade'


class Curso_escola(models.Model):
    id = models.AutoField(primary_key=True)
    escola_id = models.IntegerField()
    curso_id = models.IntegerField()
    status = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'curso_escola'


class Cadastrar_curso(models.Model):
    id = models.AutoField(primary_key=True)
    escola = models.ForeignKey(Metas_escolas, on_delete=models.CASCADE)
    tipo = models.ForeignKey(Metas_tipo, on_delete=models.CASCADE)
    eixos = models.ForeignKey(Eixos, on_delete=models.CASCADE, null=True)
    curso = models.CharField(max_length=255)
    modalidade = models.ForeignKey(Metas_modalidade, on_delete=models.CASCADE)
    status = models.CharField(max_length=255)
    escolaridade = models.CharField(max_length=255)
    idade_min = models.IntegerField()
    carga_horaria = models.IntegerField(blank=False, null=True)
    siga_id = models.IntegerField(blank=False, null=True)

    def __str__(self):
        return self.curso

    class Meta:
        managed = True
        db_table = 'cursos'
        ordering = ('curso',)


class Orcamento_plano_trabalho(models.Model):
    id = models.AutoField(primary_key=True)
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
        managed = True
        db_table = 'planejamento_trabalho'


class Udepi_municipio(models.Model):
    id = models.AutoField(primary_key=True)
    escola = models.ForeignKey(Metas_escolas, on_delete=models.CASCADE)
    municipio = models.CharField(max_length=255)

    def __str__(self):
        return self.municipio

    class Meta:
        managed = True
        db_table = 'udepi_municipio'


class Edital(models.Model):
    id = models.AutoField(primary_key=True)
    num_edital = models.IntegerField()
    ano = models.IntegerField()
    dt_ini_edit = models.DateField(null=True, blank=True)
    dt_fim_edit = models.DateField(null=True, blank=True)
    dt_ini_insc = models.DateField(null=True, blank=True)
    dt_fim_insc = models.DateField(null=True, blank=True)
    escola = models.ForeignKey(Metas_escolas, on_delete=models.CASCADE)
    status = models.CharField(max_length=255)
    pdf = models.CharField(max_length=255, null=True, blank=True)
    motivo = models.CharField(max_length=255, blank=False, null=True)
    user_change = models.ForeignKey(User,on_delete = models.DO_NOTHING,null=True)
    def __str__(self):
        return self.num_edital

    class Meta:
        managed = True
        db_table = 'edital_ensino'


class Metas_efg(models.Model):
    SITUACAO = (
        (0, 'Aguardando Análise'),
        (1, 'Reprovado'),
        (2, 'Em Análise'),
        (3, 'Aprovado'),
        (4, 'Edital gerado'),
        (5, 'Replanejado'),
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
        ('INTEGRAL', 'INTEGRAL')
    )

    id = models.AutoField(primary_key=True)
    diretoria = models.CharField(max_length=255, choices=DIRETORIAS, null=True)
    escola = models.ForeignKey(
        Metas_escolas, on_delete=models.CASCADE, null=True)
    tipo_curso = models.ForeignKey(
        Metas_tipo, on_delete=models.CASCADE, null=True)
    curso = models.ForeignKey(
        Cadastrar_curso, on_delete=models.CASCADE, null=True)
    turno = models.CharField(max_length=255, choices=TURNOS, null=True)
    ano = models.IntegerField()
    modalidade = models.ForeignKey(Metas_modalidade, on_delete=models.CASCADE)
    trimestre = models.IntegerField(choices=SEMESTRES, null=True)
    vagas_totais = models.IntegerField(null=True)
    carga_horaria = models.IntegerField(null=True)
    carga_horaria_total = models.IntegerField(null=True)
    previsao_inicio = models.DateField(null=True)
    previsao_fim = models.DateField(null=True)
    dias_semana = models.CharField(max_length=255)
    previsao_abertura_edital = models.DateField(null=True, blank=True)
    previsao_fechamento_edital = models.DateField(null=True, blank=True)
    data_registro = models.DateField(null=True, blank=True)
    eixo = models.ForeignKey(Eixos, on_delete=models.CASCADE, null=True)
    udepi = models.ForeignKey(
        Udepi_municipio, on_delete=models.CASCADE, null=True)
    situacao = models.IntegerField(
        default=0, choices=SITUACAO, null=True, blank=True)
    jus_reprovacao = models.TextField(default=None, null=True, blank=True)
    num_edital = models.ForeignKey(
        Edital, on_delete=models.CASCADE, default=None, null=True, blank=True)
    curso_tecnico = models.CharField(
        default=None, null=True, blank=True, max_length=255)
    qualificacoes = models.CharField(
        default='', null=True, blank=True, max_length=255)
    origem_replan = models.IntegerField(null=True)
    
    def get_origem_replan_data(self):
        if self.origem_replan:
            turma_origem = Metas_efg.objects.get(pk=self.origem_replan)

            return turma_origem

    def get_absolute_url(self):
        return reverse_lazy('AprovarCursosView')

    def __str__(self):
        return self.curso

    class Meta:
        managed = True
        db_table = 'Turmas_planejado_orcado'


class User_permission(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    permission = models.CharField(max_length=255)
    escola = models.ForeignKey(
        Metas_escolas, on_delete=models.DO_NOTHING, null=True)

    class Meta:
        managed = True
        db_table = 'user_permission'


class Users_ids(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    user_selecao_id = models.IntegerField()
    user_siga_id = models.IntegerField()
    cpf = models.CharField(max_length=14, null=True, default=None)

    class Meta:
        managed = True
        db_table = 'users_siga_selecao'

class Saldo_replanejamento(models.Model):
    id = models.AutoField(primary_key=True)
    tipo = models.ForeignKey(Metas_tipo,on_delete=models.DO_NOTHING)
    modalidade =  models.ForeignKey(Metas_modalidade,on_delete=models.DO_NOTHING)
    ano = models.IntegerField(default=None)
    semestre = models.IntegerField(default=None)
    saldo = models.IntegerField(default=None)

    class Meta:
        managed = True
        db_table = 'saldo_replanejamento'