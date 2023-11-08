from django.shortcuts import render, redirect
from appprojeto1.models import Saldo_replanejamento, Cadastrar_curso, Users_ids, Udepi_municipio, Edital, Curso_escola, Cursos, Eixos, Item_apoiado, Metas_tipo, Metas_descricoes, Metas_efg, Metas_escolas, Metas_modalidade, Metas_sinteticas, Metas_trimestre, Orcamento_plano_trabalho, Rubrica, Solicitacao, Unidades, User_permission, User
from DivisaoDeMetas.models import DivisaoDeMetasPorEscola
from django.core import serializers
from django.http import HttpResponse
from django.contrib import messages
import datetime
import MySQLdb
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django_tables2.views import SingleTableMixin
from django_filters.views import FilterView
from django_tables2.export.views import ExportMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django_tables2.paginators import LazyPaginator
from django.db import connection, reset_queries
from appprojeto1.forms import (
    AprovarCursosFilterFormHelper,
    AprovarCursosSubmitFormView,
    AprovarCursosForm,
    ReprovaCursosForm
)
import pyodbc
from django.shortcuts import render, get_object_or_404
from appprojeto1.tables import AprovarCursosTable
from appprojeto1.filters import AprovarCursosFilter, DashboardAprovarCursosFilter
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import FormView
from django.views.generic import UpdateView, TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
import requests as req
import json
from requests.auth import HTTPBasicAuth
from django.views.generic.base import ContextMixin
from pycamunda import task as CamundaTask
from requests import sessions, auth
from django.db.models import Q, Sum, Case, When, F
import envconfiguration as config
import json
from django.http import JsonResponse

# DADOS DO SERVIDOR
host = 'https://processos.cett.dev.br/engine-rest/'
# host = config.CAMUNDA_URL  # type: ignore
processName = "SolicitarOfertaDeVagas"
autentication = HTTPBasicAuth('dmartins', 'CETT@2022')


def getInstance(processName, taskDefinition):
    taskDefinitionKey = taskDefinition
    url = f"{host}/task?processDefinitionKey={processName}"
    requisicao = req.get(url, json={}, auth=autentication)
    retorno = requisicao.text
    json_object = json.loads(retorno)
    for dados in json_object:
        try:
            if dados['taskDefinitionKey'] == taskDefinitionKey:
                idTask = dados['id']
                headers = {'Content-type': 'application/json'}
                completeTask = req.post(
                    f"{host}/task/{idTask}/complete", auth=autentication, headers=headers)
                if completeTask.status_code == 204:
                    # print('Taks is completed!')
                    return True
                else:
                    return False
        except:
            if dados[0]['taskDefinitionKey'] == taskDefinitionKey:
                idTask = dados['id']
                headers = {'Content-type': 'application/json'}
                completeTask = req.post(
                    f"{host}/task/{idTask}/complete", auth=autentication, headers=headers)
                if completeTask.status_code == 204:
                    # print('Taks is completed!')
                    return True
                else:
                    return False


def getUserlogin(request):
    username = request.user
    id_user = User.objects.filter(username=username).values()
    return id_user[0]['id']


# # EXECUTA LOCALMENTE
# HOST = "127.0.0.1"
# USER = "root"
# PASS = ""
# DB = "c35camundadb"
# PORT = 3306

# EXECUTA NO DOCKER
HOST = "200.137.215.67"
USER = "c1camundadb"
PASS = "iC7@hdDF"
DB = "c1camundadb"
PORT = 3306

# @login_required(login_url='/')


def get_permission(request):

    user_id = getUserlogin(request)
    perm = User_permission.objects.filter(user_id=user_id).values()
    return perm[0]


def select_vagas_horas(ano, trimestre, escola, modalidade, curso, tipo, type_count):
    mydb = MySQLdb.connect(
        host=HOST,	   # seu host
        user=USER,	  # seu user
        passwd=PASS,		# sua senha
        db=DB,
        port=PORT)

    # host="127.0.0.1",	   # seu host
    # user="c35camundadb",	  # seu user
    # passwd="iC7@hdDF",		# sua senha
    # db="c35camundadb",
    # port=33306)	 # nome do seu banco de dados
    # Cria Cursor
    c = mydb.cursor()

    query = "SELECT SUM("+str(type_count)+") FROM Turmas_planejado_orcado "
    query_start = "WHERE"
    if ano:
        query += str(query_start) + " ano = '" + str(ano) + "'"
        query_start = " AND"

    if trimestre:
        query += str(query_start) + " trimestre = '" + str(trimestre) + "'"
        query_start = " AND"

    if escola:
        query += str(query_start) + " escola_id = '" + str(escola) + "'"
        query_start = " AND"

    if modalidade:
        query += str(query_start) + " modalidade_id = '" + \
            str(modalidade) + "'"
        query_start = " AND"

    if curso:
        query += str(query_start) + " curso_id = '" + str(curso) + "'"
        query_start = " AND"

    if tipo:
        query += str(query_start) + " tipo_curso_id = '" + str(tipo) + "'"
        query_start = " AND"

    # print(query)
    # Executa o comando SQL
    c.execute(query)

    # Imprimir toda a primeira c�lula de todas as linhas

    for l in c.fetchall():
        vagas = str(l[0])
        # print(vagas)
        if vagas == "None":
            vagas = "0"
        return vagas


def get_escolas(q):
    mydb = MySQLdb.connect(
        host=HOST,	   # seu host
        user=USER,	  # seu user
        passwd=PASS,		# sua senha
        db=DB,
        port=PORT)

    # host="127.0.0.1",	   # seu host
    # user="c35camundadb",	  # seu user
    # passwd="iC7@hdDF",		# sua senha
    # db="c35camundadb",
    # port=33306)	 # nome do seu banco de dados
    # Cria Cursor
    c = mydb.cursor()

    query = "SELECT * FROM Turmas_planejado_orcado " + q
    c.execute(query)

    for l in c.fetchall():
        return int(l[21])


def busca_usuario_siga(cpf):
    mydb = MySQLdb.connect(
        host='200.137.215.60',	   # seu host
        user='consulta',	  # seu user
        passwd='6XGZxc2gdx14ygv',		# sua senha
        db='DW_CETT',
        port=1443)

    c = mydb.cursor()

    query = "SELECT * FROM dbo.dUsuarios where cpf =  " + str(cpf)
    c.execute(query)

    for l in c.fetchall():
        return int(l[21])

# @login_required(login_url='/')


def select_vagas_horas_gerais():
    mydb = MySQLdb.connect(
        host=HOST,	   # seu host
        user=USER,	  # seu user
        passwd=PASS,		# sua senha
        db=DB,
        port=PORT)

    # host="127.0.0.1",	   # seu host
    # user="c35camundadb",	  # seu user
    # passwd="iC7@hdDF",		# sua senha
    # db="c35camundadb",
    # port=33306)	 # nome do seu banco de dados
    # Cria Cursor
    c = mydb.cursor()

    query = "SELECT modalidade_id,carga_horaria_total FROM Turmas_planejado_orcado "

    # Executa o comando SQL
    c.execute(query)

    # Imprimir toda a primeira c�lula de todas as linhas
    recurso_planejado = 0
    for l in c.fetchall():
        tipo = int(l[0])
        cht = int(l[1])
        if tipo == 1:
            recurso_planejado += cht * 8.34
        else:
            recurso_planejado += cht * 3.56
    return recurso_planejado


def Logout_Users(request):
    logout(request)
    return redirect('/')


def busca_escola_siga(id_escola):
    mydb = MySQLdb.connect(
        host=HOST,	   # seu host
        user=USER,	  # seu user
        passwd=PASS,		# sua senha
        db=DB,
        port=PORT)

    # host="127.0.0.1",	   # seu host
    # user="consulta",	  # seu user
    # passwd="4rVqoiDp9ahwEqqMtP49Fi",		# sua senha
    # db="c3siga",
    # port=13306)	 # nome do seu banco de dados
    # Cria Cursor
    c = mydb.cursor()

    if id_escola:
        query = "SELECT * from escolas where tipo = 1 and id = "+str(id_escola)
        c.execute(query)

        for l in c.fetchall():
            nome = str(l[4])

        return nome

    else:
        query = "SELECT id,nome from escolas where tipo = 1"
        c.execute(query)
        escolas_siga = []
        # Imprimir toda a primeira c�lula de todas as linhas

        for l in c.fetchall():
            id = str(l[0])
            nome = str(l[1])
            escolas = (id, nome)
            escolas_siga.append({'id': id, 'nome': nome})

        return escolas_siga


def busca_curso_siga(id_curso):
    mydb = MySQLdb.connect(
        host=HOST,	   # seu host
        user=USER,	  # seu user
        passwd=PASS,		# sua senha
        db=DB,
        port=PORT)

    # host="127.0.0.1",	   # seu host
    # user="consulta",	  # seu user
    # passwd="4rVqoiDp9ahwEqqMtP49Fi",		# sua senha
    # db="c3siga",
    # port=13306)	 # nome do seu banco de dados
    # Cria Cursor
    c = mydb.cursor()

    if id_curso:
        query = "SELECT nome from cursos where id = " + \
            str(id_curso)+" GROUP BY nome"
        c.execute(query)
        # Imprimir toda a primeira c�lula de todas as linhas

        for l in c.fetchall():
            nome = str(l[0])

        return nome

    else:
        query = "SELECT id,nome from cursos GROUP BY nome"
        c.execute(query)
        cursos_siga = []
        # Imprimir toda a primeira c�lula de todas as linhas

        for l in c.fetchall():
            id = str(l[0])
            nome = str(l[1])
            cursos_siga.append({'id': id, 'nome': nome})

        return cursos_siga


def busca_curso_escola_geral():

    mydb = MySQLdb.connect(
        host=HOST,	   # seu host
        user=USER,	  # seu user
        passwd=PASS,		# sua senha
        db=DB,
        port=PORT)

    # host="127.0.0.1",	   # seu host
    # user="c35camundadb",	  # seu user
    # passwd="iC7@hdDF",		# sua senha
    # db="c35camundadb",
    # port=33306)	 # nome do seu banco de dados
    # Cria Cursor
    c = mydb.cursor()

    query = "SELECT * FROM curso_escola"

    # Executa o comando SQL
    c.execute(query)
    front = []
    # Imprimir toda a primeira c�lula de todas as linhas

    for l in c.fetchall():
        id = str(l[0])
        id_escola = str(l[1])
        id_curso = str(l[2])
        status = str(l[3])
        nome_escola = busca_escola_siga(id_escola)
        nome_curso = busca_curso_siga(id_curso)
        front.append({'id': id_escola, 'escola': nome_escola, 'id_curso': id_curso,
                      'curso': nome_curso, 'status': status, 'id_registro': id})
    print(front)
    return front


def converter_data(data):
    # 14/03/2022
    data = str(data)
    dia = data[:2]
    mes = data[3:5]
    ano = data[6:]
    formato = ano + '-' + mes + '-' + dia
    return formato


def converter_casas(valor):
    valor = str(valor)
    valor = valor.replace(",", ".")
    return valor


@login_required(login_url='/')
def view_eixos(request):
 #   data = {}
 #   data['db'] = Eixos.objects.all()
    eixos = Eixos.objects.all()
    cursos = []
    return render(request, 'form-element-input.html', {'eixos': eixos, 'cursos': cursos})


@login_required(login_url='/')
def load_funcoes(request):
    eixos_id = request.GET.get('id_eixos')
    curso = Cursos.objects.filter(id_eixos=eixos_id).all()
    return render(request, 'ajax/ajax_load_funcoes.html', {'qualificacoes': curso})


def load_cht(request):
    escola = request.GET.get('escola_id')
    tipo_curso = request.GET.get('tipo_id')
    ano = request.GET.get('ano')
    modalidade = request.GET.get('modalidade_id')
    semestre = request.GET.get('semestre')

    ch_total_geral = DivisaoDeMetasPorEscola.objects.filter(
        escola=escola, tipo=tipo_curso, ano=ano, modalidade=modalidade, semestre=semestre).aggregate(
            carga_horaria__sum=Sum('carga_horaria')
    )['carga_horaria__sum']
    return render(request, 'ajax/ajax_load_cht.html', {'ch_total_geral': ch_total_geral})


def load_ch(request):
    escola = request.GET.get('escola_id')
    curso_selected = request.GET.get('curso_selected')
    tipocurso = request.GET.get('tipo_id')
    modalidade = request.GET.get('modalidade_id')
    eixo = request.GET.get('eixo_id')
    # print(str(escola)+'|'+str(curso_selected)+'|'+str(escola) +
    #       '|'+str(tipocurso)+'|'+str(modalidade)+'|'+str(eixo))
    carga_horaria = Cadastrar_curso.objects.filter(
        escola=escola, tipo=tipocurso, eixos=eixo, modalidade=modalidade, id=curso_selected).aggregate(
            carga_horaria__sum=Sum('carga_horaria')
    )['carga_horaria__sum']
    return render(request, 'ajax/ajax_load_carga_hr_curso.html', {'carga_hr': carga_horaria})


@login_required(login_url='/')
def load_cursos(request):
    escola_id = request.GET.get('escola_id')
    modalidade_id = request.GET.get('modalidade_id')
    id_tipo_curso = request.GET.get('tipo_id')
    eixos_id = request.GET.get('eixo_id')

    cursos = Cadastrar_curso.objects.filter(
        escola=escola_id, tipo=id_tipo_curso, modalidade=modalidade_id, eixos=eixos_id, status="ATIVO").all()

    return render(request, 'ajax/ajax_load_cursos.html', {'cursos': cursos})


@login_required(login_url='/')
def load_modalidade(request):
    escola_id = request.GET.get('escola_id')
    tipo_id = request.GET.get('tipo_id')
    eixos_id = request.GET.get('eixo_id')
    modalidade_id = request.GET.get('modalidade_id')
    cursos = Cadastrar_curso.objects.filter(
        escola=escola_id, tipo=tipo_id, eixos=eixos_id, modalidade=modalidade_id, status="ATIVO").all().values()

    return render(request, 'ajax/ajax_load_curso.html', {'cursos': cursos})


@login_required(login_url='/')
def load_eixos(request):
    escola_id = request.GET.get('escola_id')
    tipo_id = request.GET.get('tipo_id')
    eixos = Eixos.objects.filter(escola=escola_id, status="ATIVO").all()
    return render(request, 'ajax/ajax_load_eixos.html', {'eixos': eixos})


@login_required(login_url='/')
def load_municipios(request):
    id_escola = request.GET.get('escola_id')
    municipios = Udepi_municipio.objects.filter(escola_id=id_escola)
    return render(request, 'ajax/ajax_load_municipio.html', {'municipios': municipios})


@login_required(login_url='/')
def load_funcoes_filter(request):
    # print(request)
    info = request.GET['filter_select']
    vagas = []
    results = Metas_efg.objects.raw(
        'SELECT * FROM Turmas_planejado_orcado GROUP BY '+str(info))

    return render(request, 'ajax/ajax_load_filter.html', {'results': results, 'infos': info, 'vagas': vagas})


@login_required(login_url='/')
def load_funcoes_vagas(request):
    # print(request)
    ano = request.GET['ano']
    trimestre = request.GET['trimestre']
    escola = request.GET['escola']
    modalidade = request.GET['modalidade']
    curso = request.GET['curso']
    tipo = request.GET['tipo']

    filters = {}

    if ano:
        filters['ano'] = ano
    if trimestre:
        filters['trimestre'] = trimestre
    if escola:
        filters['escola'] = escola
    if modalidade:
        filters['modalidade'] = modalidade
    if curso:
        filters['curso'] = curso
    if tipo:
        filters['tipo_curso'] = tipo

    # idEscola = select_vagas_horas('escola',subfilter)
    vagas = Metas_efg.objects.filter(
        **filters).aggregate(
        vagas_totais__sum=Sum('vagas_totais')
    )['vagas_totais__sum']
    # vagas = select_vagas_horas(
    #     ano, trimestre, escola, modalidade, curso, tipo, 'vagas_totais')
    return render(request, 'ajax/ajax_load_vagas.html', {'vagas': vagas})


@login_required(login_url='/')
def load_funcoes_gerencia_eixo(request):

    id = request.GET['id']
    status = request.GET['status']
    eixos = Eixos.objects.get(id=id)
    if status == "ATIVO":
        eixos.status = "INATIVO"
    else:
        eixos.status = "ATIVO"
    eixos.save()
    refresh_eixo = Eixos.objects.all()
    return render(request, 'ajax/ajax_load_tbleixos.html', {'eixos': refresh_eixo})


@login_required(login_url='/')
def load_funcoes_gerencia_cursos(request):

    id = request.GET['id']
    status = request.GET['status']
    cursos = Cadastrar_curso.objects.select_related(
        'escola').select_related('tipo').select_related('eixos').get(id=id)
    if status == "ATIVO":
        cursos.status = "INATIVO"
    else:
        cursos.status = "ATIVO"
    cursos.save()
    refresh_cursos = Cadastrar_curso.objects.select_related(
        'escola').select_related('tipo').select_related('eixos').all()
    return render(request, 'ajax/ajax_load_tblcursos.html', {'cursos': refresh_cursos})


@login_required(login_url='/')
def load_funcoes_permissoes(request):
    userid = request.GET['userid']
    perm = User_permission.objects.filter(user_id=userid).values()[0]
    escolas = Metas_escolas.objects.filter(tipo__in=[0, 1])
    return render(request, 'ajax/ajax_load_permissoes.html', {'perm': perm, 'escolas': escolas})


@login_required(login_url='/')
def load_funcoes_rp(request):
    ano = request.GET['ano']
    trimestre = request.GET['trimestre']
    escola = request.GET['escola']
    modalidade = request.GET['modalidade']
    curso = request.GET['curso']
    tipo = request.GET['tipo']
    # idEscola = select_vagas_horas('escola',subfilter)
    # total_horas = select_vagas_horas(
    #     ano, trimestre, escola, modalidade, curso, tipo, 'carga_horaria_total')

    filters = {}

    if ano:
        filters['ano'] = ano
    if trimestre:
        filters['trimestre'] = trimestre
    if escola:
        filters['escola'] = escola
    if modalidade:
        filters['modalidade'] = modalidade
    if curso:
        filters['curso'] = curso
    if tipo:
        filters['tipo_curso'] = tipo
    total_horas = Metas_efg.objects.filter(
        **filters).aggregate(
        carga_horaria_total__sum=Sum(
            Case(
                When(
                    modalidade_id=1,
                    then=F('carga_horaria_total') * 8.34
                ),
                default=F('carga_horaria_total') * 3.56
            )
        )
    )['carga_horaria_total__sum']

    # vagas = select_vagas_horas(ano,trimestre,escola,modalidade,curso,tipo,'vagas_totais')
    # total_horas = int(horas) * int(vagas)

    # if modalidade == "1":
    #     rp = float(total_horas) * 8.34  # type: ignore
    # else:
    #     rp = rp = float(total_horas) * 3.56
    # print('Resultado do Recurso Planejado' + str(rp))

    return render(request, 'ajax/ajax_load_recurso_planejado.html', {'rp': total_horas})


@login_required(login_url='/')
def load_funcoes_tabela(request):
    # print(request.GET)
    ano = request.GET['ano']
    trimestre = request.GET['trimestre']
    escola = request.GET['escola']
    modalidade = request.GET['modalidade']
    curso = request.GET['curso']
    tipo = request.GET['tipo']

    query = "SELECT * FROM Turmas_planejado_orcado "
    query_start = "WHERE"
    if ano:
        query += str(query_start) + " ano = '" + str(ano) + "'"
        query_start = " AND"

    if trimestre:
        query += str(query_start) + " trimestre = '" + str(trimestre) + "'"
        query_start = " AND"

    if escola:
        query += str(query_start) + " escola_id = '" + str(escola) + "'"
        query_start = " AND"

    if modalidade:
        query += str(query_start) + " modalidade_id = '" + \
            str(modalidade) + "'"
        query_start = " AND"

    if curso:
        query += str(query_start) + " curso_id = '" + str(curso) + "'"
        query_start = " AND"

    if tipo:
        query += str(query_start) + " tipo_curso_id = '" + str(tipo) + "'"
        query_start = " AND"

    info = Metas_efg.objects.raw(query)
    return render(request, 'ajax/ajax_load_table.html', {'filtros': info})


@login_required(login_url='/')
def load_funcoes_total_horas(request):
    ano = request.GET['ano']
    trimestre = request.GET['trimestre']
    escola = request.GET['escola']
    modalidade = request.GET['modalidade']
    curso = request.GET['curso']
    tipo = request.GET['tipo']
    # total_horas = select_vagas_horas(
    #     ano, trimestre, escola, modalidade, curso, tipo, 'carga_horaria_total')

    filters = {}

    if ano:
        filters['ano'] = ano
    if trimestre:
        filters['trimestre'] = trimestre
    if escola:
        filters['escola'] = escola
    if modalidade:
        filters['modalidade'] = modalidade
    if curso:
        filters['curso'] = curso
    if tipo:
        filters['tipo_curso'] = tipo
    total_horas = Metas_efg.objects.filter(
        **filters).aggregate(
        carga_horaria_total__sum=Sum('carga_horaria_total')
    )['carga_horaria_total__sum']
    # vagas = select_vagas_horas(ano,trimestre,escola,modalidade,curso,tipo,'vagas_totais')
    # total_horas = int(horas) * int(vagas)
    return render(request, 'ajax/ajax_load_total_horas.html', {'total_horas': total_horas})


def view_geral(request):
    return render(request, 'login.html')


@csrf_protect
def Autenticar(request):
    # return render(request,"forms.html")
    if request.POST:
        username = request.POST['user']
        password = request.POST['pass']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/dashboard')
        else:
            messages.error(request, ' Usuário/Senha inválidos!')
            return redirect('/')


@login_required(login_url='/')
def view_index(request):

    user_id = getUserlogin(request)

    perm = User_permission.objects.filter(user_id=user_id).values()

    return render(request, 'index.html', {'permissoes': perm[0]})


@login_required(login_url='/')
def realizar_solicitacao(request):
    eixo = request.POST['basicInput']
    query_eixo = Eixos.objects.filter(id=eixo).values('nome')
    context_eixo = {'ex': query_eixo}
    neweixo = context_eixo['ex'][0]['nome'][0:]

    curso = request.POST['qualificacoes_id_eixos']
    query_curso = Cursos.objects.filter(id=curso).values('nome')
    context_eixo = {'ex': query_curso}
    newcurso = query_curso[0]['nome'][0:]

    modalidade = request.POST['modalidade']
    tipo = request.POST['tipo']
    justificativa = request.POST['justificativa']
    # print(eixo)
    submit = Solicitacao.objects.create(
        eixo=neweixo, curso=newcurso, modalidade=modalidade, tipo=tipo, justificativa=justificativa)
    return redirect('/eixos')


@login_required(login_url='/')
def cadastrar_metas(request):

    user_id = getUserlogin(request)
    perm = User_permission.objects.filter(user_id=user_id).values()

    perm_escolas = perm[0]['escola_id']

    tipo_curso = Metas_tipo.objects.all()
    saldoReplanejado = Saldo_replanejamento.objects.all()
    modalidade = Metas_modalidade.objects.all()
    if perm_escolas != None:
        lancamentos = Metas_efg.objects.filter(escola=perm_escolas).all()
        btn_enviar_planejamento = Metas_efg.objects.filter(
            escola_id=int(perm_escolas)).values()

        btn_enviar_planejamento_reprovados = Metas_efg.objects.filter(
            escola_id=int(perm_escolas), situacao=1).all().count()

        btn_enviar_planejamento_aanalise = Metas_efg.objects.filter(
            escola_id=int(perm_escolas), situacao=0).all().count()

        escolas_cad = Metas_escolas.objects.filter(id=perm_escolas)
    else:
        lancamentos = Metas_efg.objects.all()
        btn_enviar_planejamento = Metas_efg.objects.all()
        escolas_cad = Metas_escolas.objects.filter(tipo__in=[0, 1])

    municipios = Udepi_municipio.objects.filter(escola_id=39)
    anos = Metas_efg.objects.raw(
        "Select id,ano from Turmas_planejado_orcado GROUP BY ano")

    mod = Metas_efg.objects.raw(
        "Select id,modalidade_id from Turmas_planejado_orcado GROUP BY modalidade_id")
    trimestre = Metas_efg.objects.raw(
        "Select id,trimestre from Turmas_planejado_orcado GROUP BY trimestre")
    escolas = Metas_efg.objects.raw(
        "Select id,escola_id from Turmas_planejado_orcado GROUP BY escola_id")
    cursos_cad = Metas_efg.objects.raw(
        "Select id,curso_id from Turmas_planejado_orcado GROUP BY curso_id")
    tipos_cad = Metas_efg.objects.raw(
        "Select id,tipo_curso_id from Turmas_planejado_orcado GROUP BY tipo_curso_id")
    eixos = Eixos.objects.filter(escola=39)
    cursos = Cadastrar_curso.objects.filter(
        escola=39, tipo=0, modalidade=1, eixos=17, status="ATIVO").all()

    if perm_escolas != None:
        return render(request, 'cadastro_metas.html', {"tipos": tipo_curso,
                                                       'escolas': escolas_cad,
                                                       'modalidades': modalidade,
                                                       'lancamentos': lancamentos,
                                                       'anos': anos,
                                                       'mods': mod,
                                                       'trimestres': trimestre,
                                                       'escolas_cad': escolas,
                                                       'cursos_cad': cursos_cad,
                                                       'tipos_cad': tipos_cad,
                                                       'eixos': eixos,
                                                       'cursos': cursos,
                                                       'municipios': municipios,
                                                       'perm_escola': perm_escolas,
                                                       'btn_enviar_planejamento_reprovados': btn_enviar_planejamento_reprovados,
                                                       'btn_enviar_planejamento_aanalise': btn_enviar_planejamento_aanalise,
                                                       'permissoes': get_permission(request), 'saldoReplanejado': saldoReplanejado})
    else:
        return render(request, 'cadastro_metas.html', {"tipos": tipo_curso,
                                                       'escolas': escolas_cad,
                                                       'modalidades': modalidade,
                                                       'lancamentos': lancamentos,
                                                       'anos': anos,
                                                       'mods': mod,
                                                       'trimestres': trimestre,
                                                       'escolas_cad': escolas,
                                                       'cursos_cad': cursos_cad,
                                                       'tipos_cad': tipos_cad,
                                                       'eixos': eixos,
                                                       'cursos': cursos,
                                                       'municipios': municipios,
                                                       'perm_escola': perm_escolas,
                                                       'btn_enviar_planejamento': btn_enviar_planejamento,
                                                       'permissoes': get_permission(request), 'saldoReplanejado': saldoReplanejado})


@login_required(login_url='/')
def cad_metas(request):
    # try:
    if True:
        diretoria = request.POST['basicInput']
        escola = request.POST['escola']
        tipo_curso = request.POST['tipo']
        nome_curso = request.POST['curso']
        turno = request.POST['turno']
        ano = request.POST['ano']
        modalidade_oferta = request.POST['modalidade']
        trimestre = request.POST['trimestre']
        carga_horaria = request.POST['carga_horaria']
        carga_horaria_total = request.POST['ch_total']
        vagas_totais = request.POST['vagas_totais']
        previsao_inicio = request.POST['data_p_inicio']
        previsao_fim = request.POST['data_p_fim']
        dias_semana = request.POST['dias_semana']
        if request.POST['p_abertura_edital'] != "" and request.POST['p_fechamento_edital'] != "":
            previsao_abertura_edital = request.POST['p_abertura_edital']
            previsao_fechamento_edital = request.POST['p_fechamento_edital']
        eixos = request.POST['eixo']
        udepi = request.POST['municipio']
        curso_tecnico = request.POST['curso_tecnico']
        try:
            qualificacoes = request.POST['qualificacoes']
        except:
            qualificacoes = ''

        meta_is_exist = Metas_efg.objects.filter(escola_id=escola, tipo_curso_id=tipo_curso,
                                                 modalidade_id=modalidade_oferta, ano=ano, trimestre=trimestre, udepi=udepi, curso_id=nome_curso, previsao_inicio=previsao_inicio, previsao_fim=previsao_fim, turno=turno).values()
        # print('-------------------------------------------------------\n\n\n\n' +
        #       str(meta_is_exist))
        if meta_is_exist:
            messages.error(
                request, '): Desculpe, mas já existe uma meta adicionada com estes dados!')
            return redirect('/cadastrar-metas')
        else:
            if request.POST['p_abertura_edital'] != "" and request.POST['p_fechamento_edital'] != "":
                cadmetas = Metas_efg.objects.create(
                    diretoria=diretoria,
                    escola_id=escola,
                    tipo_curso_id=tipo_curso,
                    curso_id=nome_curso,
                    turno=turno,
                    ano=ano,
                    eixo_id=eixos,
                    modalidade_id=modalidade_oferta,
                    trimestre=trimestre,
                    carga_horaria=carga_horaria,
                    vagas_totais=vagas_totais,
                    carga_horaria_total=carga_horaria_total,
                    previsao_inicio=previsao_inicio,
                    previsao_fim=previsao_fim,
                    dias_semana=dias_semana,
                    previsao_abertura_edital=previsao_abertura_edital,  # type: ignore
                    previsao_fechamento_edital=previsao_fechamento_edital,  # type: ignore
                    jus_reprovacao='',
                    udepi_id=udepi,
                    curso_tecnico=curso_tecnico,
                    qualificacoes=qualificacoes,
                    num_edital_id=0,
                )
            else:
                cadmetas = Metas_efg.objects.create(
                    diretoria=diretoria,
                    escola_id=escola,
                    tipo_curso_id=tipo_curso,
                    curso_id=nome_curso,
                    turno=turno,
                    ano=ano,
                    eixo_id=eixos,
                    modalidade_id=modalidade_oferta,
                    trimestre=trimestre,
                    carga_horaria=carga_horaria,
                    vagas_totais=vagas_totais,
                    carga_horaria_total=carga_horaria_total,
                    previsao_inicio=previsao_inicio,
                    previsao_fim=previsao_fim,
                    dias_semana=dias_semana,
                    jus_reprovacao='',
                    udepi_id=udepi,
                    curso_tecnico=curso_tecnico,
                    qualificacoes=qualificacoes,
                    num_edital_id=0,
                )

            if 'btn-check-2-outlined' in request.POST:
                idTurmaOrigem = int(request.POST['idOrigem'])
                idSaldoReplanejado = int(request.POST['idSaldo'])

                # ATUALIZA A TABELA DE TURMAS PARA INFORMAR QUAL FOI A ORIGEM DO REPLANEJAMENTO
                turmasParaReplanejar = Metas_efg.objects.get(id=cadmetas.id)
                turmasParaReplanejar.origem_replan = idTurmaOrigem
                turmasParaReplanejar.save()

                # OBTÉM O SALDO ATUAL DA NOVA TABELA
                saldoReplanejamento = Saldo_replanejamento.objects.filter(
                    id=idSaldoReplanejado).first()
                saldoReplan = int(saldoReplanejamento.saldo)
                novo_saldo = saldoReplan - int(carga_horaria_total)

                # ATUALIZA O SALDO UTILIZADO NA TABELA DE SALDOS DE REPLANEJAMENTO
                saldoReplanejamento.saldo = novo_saldo
                saldoReplanejamento.save()

                messages.success(
                    request, 'A meta cadastrada com replanejamento foi realizada com sucesso!')
                return redirect('/cadastrar-metas')
            else:
                # BUSCA OS DADOS DA META DE ACORDO COM OS FILTROS SETADOS NA META
                atualiza_saldo = DivisaoDeMetasPorEscola.objects.filter(
                    escola=escola, tipo=tipo_curso, modalidade=modalidade_oferta, semestre=trimestre, ano=ano).values()

                # ID DA META A QUAL DEVERÁ ATUALIZAR
                id_filtro = atualiza_saldo[0]['id']

                # CARGA HORÁRIA TOTAL DA META
                cht_meta = carga_horaria_total

                # CARGA HORÁRIA TOTAL DA DIVISÃO
                cht_divisao = int(atualiza_saldo[0]['carga_horaria_total'])

                # CARGA HORÁRIA DISPONÍVEL DA META
                cht_disponivel_divisao = int(
                    atualiza_saldo[0]['carga_horaria'])

                # SALDO A DEBITAR
                saldo_total = int(cht_disponivel_divisao) - int(cht_meta)
                atualiza_saldo = DivisaoDeMetasPorEscola.objects.get(
                    id=id_filtro)

                atualiza_saldo.created_at = datetime.datetime.now()
                atualiza_saldo.carga_horaria = saldo_total
                atualiza_saldo.save()
                messages.success(request, 'Meta cadastrada com sucesso!')
                return redirect('/cadastrar-metas')
    # except:
    #     pass


@login_required(login_url='/')
def apagar_meta(request):
    codigo = request.POST['id_deleta']
    # escola = request.POST['escola_delete']
    # tipo_curso = request.POST['tipo_delete']
    # ano = request.POST['ano_delete']
    # carga_horaria_total = request.POST['cht']

    metas_filtro = Metas_efg.objects.filter(id=codigo).values()
    # print(metas_filtro[0])
    escola = metas_filtro[0]['escola_id']
    tipo_curso = metas_filtro[0]['tipo_curso_id']
    modalidade = metas_filtro[0]['modalidade_id']
    ano = metas_filtro[0]['ano']
    ch_total = metas_filtro[0]['carga_horaria_total']
    semestre = metas_filtro[0]['trimestre']

    meta = Metas_efg.objects.get(id=codigo)
    meta.delete()
    # semestre e modalidade
    atualiza_saldo = DivisaoDeMetasPorEscola.objects.filter(
        escola=escola, tipo=tipo_curso, ano=ano, modalidade=modalidade, semestre=semestre).values()
    id_filtro = atualiza_saldo[0]['id']
    novo_saldo = int(
        atualiza_saldo[0]['carga_horaria']) + int(ch_total)
    atualiza_divisao = DivisaoDeMetasPorEscola.objects.get(id=id_filtro)
    atualiza_divisao.carga_horaria = novo_saldo
    atualiza_divisao.save()
    messages.success(request, 'Meta removida com sucesso!')
    return redirect('/cadastrar-metas')


@login_required(login_url='/')
def editar_meta(request, codigo):
    infoFiltro = Metas_efg.objects.filter(id=codigo).values()
    meta_edit = Metas_efg.objects.get(id=codigo)
    pega_eixos = Metas_efg.objects.filter(id=codigo).values()
    diretoria = pega_eixos[0]['diretoria']
    idEscola = pega_eixos[0]['escola_id']
    idMunicipio = pega_eixos[0]['udepi_id']
    tipoCursos = pega_eixos[0]['tipo_curso_id']
    idEixos = pega_eixos[0]['eixo_id']
    idModalidade = pega_eixos[0]['modalidade_id']
    idCurso = int(pega_eixos[0]['curso_id'])
    turno = pega_eixos[0]['turno']
    ano = pega_eixos[0]['ano']
    trimestre = int(pega_eixos[0]['trimestre'])
    ch = int(pega_eixos[0]['carga_horaria'])
    qtdVagas = int(pega_eixos[0]['vagas_totais'])
    cht = int(pega_eixos[0]['carga_horaria_total'])
    pi = pega_eixos[0]['previsao_inicio']
    pi = datetime.datetime.strftime(pi, '%Y-%m-%d')
    pf = pega_eixos[0]['previsao_fim']
    pf = datetime.datetime.strftime(pf, '%Y-%m-%d')
    dia_semana = pega_eixos[0]['dias_semana']
    idEdit = pega_eixos[0]['id']
    jus_reprovacao = pega_eixos[0]['jus_reprovacao']
    curso_tecnico = pega_eixos[0]['curso_tecnico']
    qualificacoes = pega_eixos[0]['qualificacoes']
    tipos_cursos = Metas_tipo.objects.all()

    escolas = Metas_escolas.objects.filter(tipo=0)
    eixos = Eixos.objects.filter(escola_id=idEscola)
    modalidades = Metas_modalidade.objects.all()
    municipios = Udepi_municipio.objects.filter(escola_id=idEscola)

    cursos = Cadastrar_curso.objects.filter(eixos=idEixos, tipo_id=tipoCursos)
    # print(infoFiltro[0]['escola_id'], infoFiltro[0]
    #       ['tipo_curso_id'], infoFiltro[0]['ano'])
    atualiza_saldo = DivisaoDeMetasPorEscola.objects.filter(
        escola=infoFiltro[0]['escola_id'], tipo=infoFiltro[0]['tipo_curso_id'], ano=infoFiltro[0]['ano']).values()

    # id_filtro = atualiza_saldo[0]['id']
    limite = atualiza_saldo[0]['carga_horaria']

    return render(request, 'editar_metas.html', {'meta_edit': meta_edit,
                                                 'tipos_cursos': tipos_cursos,
                                                 'modalidades': modalidades,
                                                 'escolas': escolas,
                                                 'eixos': eixos,
                                                 'cursos': cursos,
                                                 'limite': limite,
                                                 'municipios': municipios,
                                                 'diretoria': diretoria,
                                                 'idEscola': idEscola,
                                                 'idMunicipio': idMunicipio,
                                                 'tipoCursos': tipoCursos,
                                                 'idEixos': idEixos,
                                                 'idModalidade': idModalidade,
                                                 'idCurso': idCurso,
                                                 'turno': turno,
                                                 'ano': ano,
                                                 'trimestre': trimestre,
                                                 'ch': ch,
                                                 'qtdVagas': qtdVagas,
                                                 'cht': cht,
                                                 'pi': pi,
                                                 'pf': pf,
                                                 'dia_semana': dia_semana,
                                                 'idEdit': idEdit,
                                                 'permissoes': get_permission(request),
                                                 'jus_reprovacao': jus_reprovacao,
                                                 'curso_tecnico': curso_tecnico,
                                                 'qualificacoes': qualificacoes})


@login_required(login_url='/')
def editarmetas(request):

    id_ = request.POST['id']

    diretoria = request.POST['diretoria']
    escola = request.POST['escola']
    municipio = request.POST['municipio']

    tipo_curso = request.POST['tipo']
    eixos = request.POST['eixo']
    modalidade_oferta = request.POST['modalidade']
    nome_curso = request.POST['curso']
    turno = request.POST['turno']
    ano = request.POST['ano']
    trimestre = request.POST['trimestre']
    carga_horaria = request.POST['carga_horaria']
    vagas_totais = request.POST['vagas_totais']
    carga_horaria_total = request.POST['ch_total']
    previsao_inicio = request.POST['data_p_inicio']
    # previsao_inicio = converter_data(previsao_inicio)
    previsao_fim = request.POST['data_p_fim']
    # previsao_fim = converter_data(previsao_fim)
    dias_semana = request.POST['dias_semana']

    curso_tecnico = request.POST['curso_tecnico']
    qualificacao = request.POST['qualificacoes']

    editmetas = Metas_efg.objects.get(id=id_)
    editmetas.udepi_id = municipio  # type: ignore
    editmetas.diretoria = diretoria
    editmetas.escola_id = escola  # type: ignore
    editmetas.tipo_curso_id = tipo_curso  # type: ignore
    editmetas.eixo_id = eixos  # type: ignore
    editmetas.curso_id = nome_curso  # type: ignore
    editmetas.turno = turno
    editmetas.ano = ano
    editmetas.modalidade_id = modalidade_oferta  # type: ignore
    editmetas.trimestre = trimestre
    editmetas.carga_horaria = carga_horaria
    editmetas.carga_horaria_total = carga_horaria_total
    editmetas.vagas_totais = vagas_totais
    editmetas.previsao_inicio = previsao_inicio
    editmetas.previsao_fim = previsao_fim
    editmetas.dias_semana = dias_semana
    editmetas.curso_tecnico = curso_tecnico
    editmetas.qualificacoes = qualificacao
    editmetas.save()

    # BUSCA OS DADOS DA META DE ACORDO COM OS FILTROS SETADOS NA META
    atualiza_saldo = DivisaoDeMetasPorEscola.objects.filter(
        escola=escola, tipo=tipo_curso, modalidade=modalidade_oferta, semestre=trimestre, ano=ano).values()

    # ID DA META A QUAL DEVERÁ ATUALIZAR
    id_filtro = atualiza_saldo[0]['id']

    # VALOR ORIGINAL DA META
    cht_original_meta = int(request.POST['cht_meta'])

    # CARGA HORÁRIA TOTAL DA META
    cht_meta = carga_horaria_total

    # CARGA HORÁRIA TOTAL DA DIVISÃO
    cht_divisao = int(atualiza_saldo[0]['carga_horaria_total'])

    # CARGA HORÁRIA DISPONÍVEL DA META
    cht_disponivel_divisao = int(
        atualiza_saldo[0]['carga_horaria']) + int(cht_original_meta)

    # SALDO A DEBITAR
    saldo_total = int(cht_disponivel_divisao) - int(cht_meta)
    atualiza_saldo = DivisaoDeMetasPorEscola.objects.get(id=id_filtro)

    atualiza_saldo.created_at = datetime.datetime.now()
    atualiza_saldo.carga_horaria = saldo_total
    atualiza_saldo.save()

    messages.success(request, 'Meta editada com sucesso!')
    return redirect('/cadastrar-metas')


@login_required(login_url='/')
def cadastrar_meta_sintetica(request):
    escolas = Metas_escolas.objects.filter(tipo__in=[0, 1])
    tipo_curso = Metas_tipo.objects.all()
    modalidade = Metas_modalidade.objects.all()
    trimestre = Metas_trimestre.objects.all()
    descricao = Metas_descricoes.objects.all()
    reset_queries()
    meta_sintetica = Metas_sinteticas.objects.select_related(
        'escola', 'modalidade').all()
    # print(connection.queries)
    # print(meta_sintetica)
    eixos = Eixos.objects.all()
    return render(request, 'cadastro_metas_sinteticas.html', {'meta_sinteticas': meta_sintetica,
                                                              'escolas': escolas,
                                                              'tipos_curso': tipo_curso,
                                                              'modalidades': modalidade,
                                                              'trimestres': trimestre,
                                                              'descricoes': descricao,
                                                              'eixos': eixos,
                                                              'permissoes': get_permission(request)})


@login_required(login_url='/')
def cad_metas_sintetica(request):

    diretoria = request.POST['basicInput']
    escola = request.POST['escola']
    ano = request.POST['ano']
    modalidade = request.POST['modalidade']
    tipo = request.POST['tipo']
    descricao = request.POST['descricao']
    ch_ofertada = request.POST['ch_ofertada']
    vagas = request.POST['vagas']
    repasse = request.POST['repasse']
    repasse = converter_casas(repasse)
    valor_unitario = request.POST['valor_unitario']

    cadmetas = Metas_sinteticas.objects.create(diretoria=diretoria,
                                               escola_id=escola,
                                               ano=ano,
                                               modalidade_id=modalidade,
                                               categoria_id=tipo,
                                               descricao_id=descricao,
                                               ch_ofertada=ch_ofertada,
                                               vagas=vagas,
                                               repasse=repasse,
                                               valor_unitario=valor_unitario)

    messages.success(request, 'Meta cadastrada com sucesso!')
    return redirect('/cadastrar-metas-sinteticas')


@login_required(login_url='/')
def apagar_meta_sintetica(request):
    codigo = request.POST['id_deleta']
    meta = Metas_sinteticas.objects.get(id=codigo)
    meta.delete()
    messages.success(request, 'Meta removida com sucesso!')
    return redirect('/cadastrar-metas-sinteticas')


@login_required(login_url='/')
def editar_metas_sintetica(request):
    id_ = request.POST['id_edit']
    diretoria = request.POST['basicInputModal2']
    escola = request.POST['escola2']
    ano = request.POST['ano2']
    modalidade = request.POST['modalidade2']
    tipo = request.POST['tipo2']
    descricao = request.POST['descricao2']
    ch_ofertada = request.POST['ch_ofertada2']
    vagas = request.POST['vagas2']
    repasse = request.POST['repasse2']
    valor_unitario = request.POST['valor_unitario2']

    editMetasS = Metas_sinteticas.objects.get(id=id_)
    editMetasS.diretoria = diretoria
    editMetasS.escola_id = escola  # type: ignore
    editMetasS.ano = ano
    editMetasS.modalidade_id = modalidade  # type: ignore
    editMetasS.descricao_id = descricao  # type: ignore
    editMetasS.tipo_id = tipo  # type: ignore
    editMetasS.ch_ofertada = ch_ofertada
    editMetasS.vagas = vagas
    editMetasS.repasse = repasse
    editMetasS.valor_unitario = valor_unitario

    editMetasS.save()
    messages.success(request, 'Meta editada com sucesso!')
    return redirect('/cadastrar-metas-sinteticas')


@login_required(login_url='/')
def orcamento_plano_trabalho(request):
    planejamento = Orcamento_plano_trabalho.objects.all()
    rubrica = Rubrica.objects.all()
    unidades = Unidades.objects.all()
    item_apoiado = Item_apoiado.objects.all()
    centro_custo = []
    return render(request, 'orcamento_plano_trabalho.html', {'rubricas': rubrica, 'centro_custo': centro_custo, 'unidades': unidades, 'planejamentos': planejamento, 'itens_apoiados': item_apoiado, 'permissoes': get_permission(request)})


@login_required(login_url='/')
def rubrica(request):
    rubrica = Rubrica.objects.all()
    centro_custo = []
    return render(request, 'orcamento_plano_trabalho.html', {'rubricas': rubrica, 'centro_custo': centro_custo})


@login_required(login_url='/')
def load_funcoes_rubrica(request):
    ia_id = request.GET.get('id_rubrica')
    item_apoiado = Item_apoiado.objects.filter(id_rubrica=ia_id).all()
    return render(request, 'ajax/ajax_load_item_apoiado.html', {'itens_apoiados': item_apoiado})


@login_required(login_url='/')
def cad_orcamento(request):
    receita = request.POST['tipo']
    rubrica = request.POST['rubrica']
    item_apoiado = request.POST['item_apoiado']
    und = request.POST['unidade']
    qtd_global = request.POST['qtd_global']
    qtd_global = converter_casas(qtd_global)
    valor_medio_unitario = request.POST['v_m_unitario']
    valor_medio_unitario = converter_casas(valor_medio_unitario)
    valor_global = request.POST['valor_global']
    valor_global = converter_casas(valor_global)
    custeio = request.POST['custeio']
    custeio = converter_casas(custeio)
    capital = request.POST['capital']
    capital = converter_casas(capital)

    orcamento = Orcamento_plano_trabalho.objects.create(
        tipo=receita,
        rubrica_id=rubrica,
        item_apoiado_id=item_apoiado,
        und=und,
        qtd_global=qtd_global,
        valor_medio_unitario=valor_medio_unitario,
        valor_global=valor_global,
        custeio=custeio,
        capital=capital

    )
    messages.success(request, 'Orçamento cadastrado com sucesso!')
    return redirect('/orcamento-plano-trabalho')


@login_required(login_url='/')
def editar_orcamento(request):

    id_ = request.POST['id_edit']
    tipo = request.POST['tipo2']
    rubrica = request.POST['rubrica2']
    item_apoiado = request.POST['item_apoiado2']
    unidade = request.POST['unidade2']
    qtd_global = request.POST['qtd_global2']
    v_m_unitario = request.POST['v_m_unitario2']
    valor_global = request.POST['valor_global2']
    custeio = request.POST['custeio2']
    capital = request.POST['capital2']

    editorcamento = Orcamento_plano_trabalho.objects.get(id=id_)
    editorcamento.tipo = tipo
    editorcamento.rubrica_id = rubrica  # type: ignore
    editorcamento.item_apoiado_id = item_apoiado  # type: ignore
    editorcamento.und = unidade
    editorcamento.qtd_global = qtd_global
    editorcamento.valor_medio_unitario = v_m_unitario
    editorcamento.valor_global = valor_global
    editorcamento.custeio = custeio
    editorcamento.capital = capital
    editorcamento.save()
    messages.success(request, 'Orçamento editado com sucesso!')
    return redirect('/orcamento-plano-trabalho')


@login_required(login_url='/')
def apaga_orcamento(request):
    codigo = request.POST['id_deleta']
    meta = Orcamento_plano_trabalho.objects.get(id=codigo)
    meta.delete()
    messages.success(request, 'Orçamento removido com sucesso!')
    return redirect('/orcamento-plano-trabalho')


@login_required(login_url='/')
def cadastro_curso_escola(request):
    escolas = Metas_escolas.objects.filter(tipo__in=[0, 1]).values()
    # print(escolas)
    curso = Cadastrar_curso.objects.all()
    return render(request, 'cadastro_curso_escola.html', {'escolas': escolas, 'cursos': curso, 'permissoes': get_permission(request)})


@login_required(login_url='/')
def cad_curso_escola(request):
    escola = request.POST['escola']
    curso = request.POST['curso']
    status = request.POST['status']

    cadmetas = Curso_escola.objects.create(
        escola_id=escola, curso_id=curso, status=status)

    messages.success(request, 'Curso cadastrado na escola selecionada!')
    return redirect('/cadastrar-curso-escola')


@login_required(login_url='/')
def apagar_curso_escola(request):
    codigo = request.POST['id_deleta']
    curso = Curso_escola.objects.get(id=codigo)
    # print(curso)
    curso.delete()
    messages.success(request, 'Curso removido desta escola!')
    return redirect('/cadastrar-curso-escola')


@login_required(login_url='/')
def editar_curso_escola(request):
    id_ = request.POST['id_edit']
    # print(id_)
    escola_id = request.POST['escola_modal']
    curso_id = request.POST['curso_modal']
    status = request.POST['status_modal']
    editCursoEscola = Curso_escola.objects.get(id=id_)
    editCursoEscola.escola_id = escola_id
    editCursoEscola.curso_id = curso_id
    editCursoEscola.status = status

    editCursoEscola.save()
    messages.success(request, 'Registros alterados com sucesso!')
    return redirect('/cadastrar-curso-escola')


@login_required(login_url='/')
def cadastrar_curso(request):
    cursos = Cadastrar_curso.objects.select_related(
        'escola').select_related('tipo').select_related('eixos').all()
    tipos = Metas_tipo.objects.all()
    eixos = Eixos.objects.all()
    escolas_cursos = Cadastrar_curso.objects.raw(
        'Select * from cursos group by escola_id')
    tipo_cursos = Cadastrar_curso.objects.raw(
        'Select * from cursos group by tipo_id')
    eixos_curso = Cadastrar_curso.objects.raw(
        'Select * from cursos group by eixos_id')
    modalidade = Metas_modalidade.objects.all()
    escolas = Metas_escolas.objects.filter(tipo__in=[0, 1]).all()
    eixos_inicial = Eixos.objects.select_related('escola').filter(escola_id=39)
    return render(request, 'cadastro_curso.html', {"cursos": cursos, 'tipos': tipos, 'eixos': eixos, 'escolas_cursos': escolas_cursos, 'tipo_curso': tipo_cursos, 'eixos_curso': eixos_curso, 'eixos_inicial': eixos_inicial, 'modalidades': modalidade, 'escolas': escolas, 'permissoes': get_permission(request)})


@login_required(login_url='/')
def cad_novo_curso(request):
    escola = request.POST['escola']
    tipo = request.POST['tipo']
    eixos = request.POST['eixo']
    curso = request.POST['curso']
    status = request.POST['status']
    modalidade = request.POST['modalidade']
    escolaridade = request.POST['escolaridade']
    carga_horaria = request.POST['carga_horaria']
    idade_minima = request.POST['idade_min']
    siga_id = request.POST['siga_id']
    cadCurso = Cadastrar_curso.objects.create(escola_id=escola, tipo_id=tipo, eixos_id=eixos, curso=curso, status=status,
                                              modalidade_id=modalidade, escolaridade=escolaridade, carga_horaria=carga_horaria, idade_min=idade_minima,
                                              siga_id=siga_id)

    messages.success(request, 'Curso cadastrado!')
    return redirect('/cadastrar-curso')


@login_required(login_url='/')
def del_curso(request):
    codigo = request.POST['id_deleta']
    curso = Cadastrar_curso.objects.get(id=codigo)
    print(curso)
    curso.delete()
    messages.success(request, 'Curso removido desta escola!')
    return redirect('/cadastrar-curso')


@login_required(login_url='/')
def editar_curso(request):
    id_ = request.POST['id_edit']
    escola = request.POST['escola_modal']
    tipo = request.POST['tipo_modal']
    modalidade = request.POST['modalidade_modal']
    escolaridade = request.POST['escolaridade_modal']
    idade_min = request.POST['idade_min_modal']
    eixos = request.POST['eixo_modal']
    curso = request.POST['curso_modal']
    status = request.POST['status_modal']
    carga_horaria = request.POST['carga_horaria_modal']
    siga_id = request.POST['siga_id_modal']
    editaCurso = Cadastrar_curso.objects.get(id=id_)
    editaCurso.escola_id = escola  # type: ignore
    editaCurso.tipo_id = tipo  # type: ignore
    editaCurso.escolaridade = escolaridade
    editaCurso.idade_min = idade_min
    editaCurso.eixos_id = eixos  # type: ignore
    editaCurso.curso = curso
    editaCurso.carga_horaria = carga_horaria
    editaCurso.status = status
    editaCurso.siga_id = siga_id
    editaCurso.modalidade_id = modalidade
    editaCurso.save()
    messages.success(request, 'Registros alterados com sucesso!')
    return redirect('/cadastrar-curso')


@login_required(login_url='/')
def cadastrar_udepi(request):
    escolas = Metas_escolas.objects.filter(tipo=0)
    udepis = Udepi_municipio.objects.all()
    return render(request, 'cadastrar_udepi.html', {'escolas': escolas, 'udepis': udepis})


class AuthenticationContextMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permissoes'] = get_permission(self.request)  # type: ignore
        return context


class FilteredSingleTableView(SingleTableMixin, FilterView):
    formhelper_class = None

    def get_filterset(self, filterset_class):
        kwargs = self.get_filterset_kwargs(filterset_class)

        if 'clean' in self.request.GET:
            kwargs['data'] = None

        filterset = filterset_class(**kwargs)
        filterset.form.helper = self.formhelper_class()
        return filterset

    def get_queryset(self):
        return Metas_efg.objects.filter(~Q(situacao__in=[4]))


class AprovarCursosView(
    LoginRequiredMixin,
    ExportMixin,
    FilteredSingleTableView,
    FormView,
    AuthenticationContextMixin
):
    login_url = '/'
    table_class = AprovarCursosTable
    table_pagination = False
    filterset_class = AprovarCursosFilter
    formhelper_class = AprovarCursosFilterFormHelper
    exclude_columns = ('actions', 'situacao', )
    form_class = AprovarCursosSubmitFormView
    success_url = reverse_lazy('AprovarCursosView')

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if 'aprovar_selecionados' in self.request.POST:
            id_list = form.data.getlist('checkbox')

            for id in range(0, len(id_list)):
                Metas_efg.objects.filter(
                    pk=id_list[id]).update(situacao=3, jus_reprovacao='')

        if 'aprovar' in self.request.POST:

            id_list = form.data.getlist('id')  # type: ignore
            action_list = form.data.getlist('situacao')  # type: ignore

            disapproved_list = list()
            for id in range(0, len(id_list)):
                if action_list[id] != '1':
                    Metas_efg.objects.filter(
                        pk=id_list[id]).exclude(
                            situacao=action_list[id]).update(
                        situacao=action_list[id], jus_reprovacao='')
                else:
                    disapproved_list.append(id_list[id])

            if disapproved_list:
                request.session['params'] = {
                    'pks': disapproved_list, 'action': 1}
                return HttpResponseRedirect(reverse('ReprovaCursosUpdateView'))

        elif 'edital' in self.request.POST:
            CamundaSession = sessions.Session()
            CamundaSession.auth = auth.HTTPBasicAuth(
                username='admin',
                password='CETT@root.8401'
            )

            GetTasks = CamundaTask.GetList(
                url=config.CAMUNDA_URL,
                task_definition_key='VerificaOPlanejamentoDeTurmasEAprovareprovaCOTECEFGTask',
            )

            GetTasks.session = CamundaSession

            tasklist = GetTasks()

            ApprovalList = set(
                Metas_efg.objects.filter(
                    situacao__in=[0, 1, 2, 3]
                ).values_list('situacao', flat=True))

            ApprovalLen = len(ApprovalList)

            ApprovalType = list(ApprovalList)[0]

            if len(tasklist) > 0 and ApprovalLen == 1 and ApprovalType == 3:
                for task in tasklist:
                    complete = CamundaTask.Complete(
                        url=config.CAMUNDA_URL,
                        id_=task.id_
                    )
                    complete.add_variable(
                        name='aprovacaodoscursos',
                        value=0,
                        type_='Integer'
                    )
                    complete.session = CamundaSession

                    complete()

                    Metas_efg.objects.filter(situacao=3).update(situacao=4)

                messages.success(
                    self.request, 'Planejamento de turmas foi aprovado')
            elif len(tasklist) == 0 and ApprovalLen == 1:
                messages.error(
                    self.request, 'Não foi encontrado tarefas para de aprovar o planejamento de turma')
            elif ApprovalLen > 1:
                messages.warning(
                    self.request, 'Para ter aprovação do planejamento de turmas, todas as turmas deveram ser aprovadas'
                )

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class AprovarCursosUpdateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    UpdateView,
    AuthenticationContextMixin
):
    login_url = '/'
    form_class = AprovarCursosForm
    model = Metas_efg
    success_url = reverse_lazy('AprovarCursosView')

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()  # type: ignore
            messages.success(self.request, 'Cadastro atualizado com sucesso')
        return super().form_valid(form)

    def form_invalid(self, form):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if not form.is_valid():
            messages.error(self.request, form._errors)  # type: ignore
        return self.render_to_response(self.get_context_data(form=form))


class ReprovaCursosUpdateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    FormView,
    AuthenticationContextMixin
):
    login_url = '/'
    form_class = ReprovaCursosForm
    model = Metas_efg
    template_name = 'appprojeto1/reprova_cursos_form.html'
    success_url = reverse_lazy('AprovarCursosView')

    def form_valid(self, form):
        params = self.request.session.get('params')
        if 'pks' in params:  # type: ignore
            selected_objects = Metas_efg.objects.filter(
                id__in=params['pks']).exclude(situacao='1')  # type: ignore
            selected_objects.update(
                situacao=params['action'], jus_reprovacao=form.cleaned_data['jus_reprovacao'])  # type: ignore

            CamundaSession = sessions.Session()
            CamundaSession.auth = auth.HTTPBasicAuth(
                username='admin',
                password='CETT@root.8401'
            )

            GetTasks = CamundaTask.GetList(
                url=config.CAMUNDA_URL,
                task_definition_key='VerificaOPlanejamentoDeTurmasEAprovareprovaCOTECEFGTask',
            )

            GetTasks.session = CamundaSession

            tasklist = GetTasks()

            if len(tasklist) > 0:
                for task in tasklist:
                    complete = CamundaTask.Complete(
                        url=config.CAMUNDA_URL,
                        id_=task.id_
                    )

                    complete.add_variable(
                        name='aprovacaodoscursos',
                        value=1,
                        type_='Integer'
                    )

                    escolas = Metas_efg.objects.filter(
                        id__in=params['pks']).values_list('escola', flat=True)
                    mails = json.dumps(list(Metas_escolas.objects.filter(
                        id__in=escolas).values('email')))

                    print(mails)
                    complete.add_variable(
                        name='emailsEscolasReprovadas',
                        value=mails,
                        type_='Json'
                    )

                    complete.session = CamundaSession

                    # print(complete)

                    complete()
            else:
                messages.error(
                    self.request, 'Não foram encontradas as tarefas de aprovação')

        return HttpResponseRedirect(reverse('AprovarCursosView'))


class DashboardAprovarCursosView(
    LoginRequiredMixin,
    AuthenticationContextMixin,
    FilterView
):
    login_url = '/'
    filterset_class = DashboardAprovarCursosFilter
    template_name = 'appprojeto1/dashboard_cursos_form.html'
    context_object_name = 'filter'

    def get_filterset(self, filterset_class):
        kwargs = self.get_filterset_kwargs(filterset_class)

        if 'clean' in self.request.GET:
            filterset = filterset_class()
        else:
            filterset = filterset_class(**kwargs)

        return filterset


@login_required(login_url='/')
def get_cursos(request):
    filtro = {}
    if request.GET.get('id_escola'):
        filtro['escola'] = request.GET.get('id_escola')
    else:
        filtro['escola'] = None
    if request.GET.get('id_modalidade'):
        filtro['modalidade'] = request.GET.get('id_modalidade')
    else:
        filtro['modalidade'] = None
    if request.GET.get('id_tipo_curso'):
        filtro['tipo'] = request.GET.get('id_tipo_curso')
    if request.GET.get('id_eixo'):
        filtro['eixos'] = request.GET.get('id_eixo')

    cursos = Cadastrar_curso.objects.filter(**filtro).values(
        'id', 'curso').order_by('curso')
    return JsonResponse(list(cursos), safe=False)


@login_required(login_url='/')
def get_eixos(request):
    filtro = {}
    if request.GET.get('id_escola'):
        filtro['escola'] = request.GET.get('id_escola')
    else:
        filtro['escola'] = None

    eixos = Eixos.objects.filter(**filtro).values('eixo_id', 'nome')
    return JsonResponse(list(eixos), safe=False)


@login_required(login_url='/')
def verifica_turmas_edital(request):

    metas = Edital.objects.raw("Select DISTINCT * from Turmas_planejado_orcado INNER JOIN edital_ensino ON Turmas_planejado_orcado.num_edital_id = edital_ensino.id INNER JOIN tipo_curso ON Turmas_planejado_orcado.tipo_curso_id = tipo_curso.id INNER JOIN modalidade ON Turmas_planejado_orcado.modalidade_id = modalidade.id where dt_ini_edit is NULL group by Turmas_planejado_orcado.num_edital_id")

    return render(request, 'verificacao_turmas_edital.html', {'metas': metas, 'permissoes': get_permission(request)})


@login_required(login_url='/')
def ajax_load_turmas_edital(request):
    edital_id = request.GET['id']
    edital = Edital.objects.filter(id=edital_id).all()
    edital = edital[0]
    lancamentos = Metas_efg.objects.all()
    return render(request, 'ajax/ajax_load_turmas_edital.html', {'edital': edital, 'lancamentos': lancamentos})


@login_required(login_url='/')
def ajax_load_turmas_edital_filtro(request):
    edital_id = request.GET['id']
    lancamentos = Metas_efg.objects.filter(num_edital_id=edital_id).all()
    # print(lancamentos.values())
    return render(request, 'ajax/ajax_load_turmas_edital_filtro.html', {'lancamentos': lancamentos})


@login_required(login_url='/')
def atualiza_edital(request):
    edital_id = request.POST['edital']
    data_ini_edit = request.POST['data_ini_edit']
    data_fim_edit = request.POST['data_fim_edit']
    data_ini_insc = request.POST['data_ini_insc']
    data_fim_insc = request.POST['data_fim_insc']
    edital_update = Edital.objects.get(id=edital_id)
    edital_update.dt_ini_edit = data_ini_edit
    edital_update.dt_fim_edit = data_fim_edit
    edital_update.dt_ini_insc = data_ini_insc
    edital_update.dt_fim_insc = data_fim_insc
    edital_update.status = 0  # type: ignore
    edital_update.save()

    edital_null = int(Edital.objects.filter(dt_ini_edit__isnull=True).count())
    if edital_null == 0:
        completeTask = getInstance(
            processName, "DefinirDatasDeEditalEDeInscricaoTask")
        messages.success(
            request, 'Edital atualizado com sucesso! Task completada!')
    else:
        messages.success(request, 'Edital atualizado com sucesso!')

    return redirect('/verifica-turmas-edital')


@login_required(login_url='/')
def gerenciar_usuarios(request):
    users = User.objects.all().order_by('username')
    escolas = Metas_escolas.objects.filter(tipo__in=[0, 1])
    return render(request, 'user_perm.html', {'users': users, 'permissoes': get_permission(request), 'escolas': escolas})

# ima,ims,opt,cc,dm,ac,vte,sicge,sat,gpu


@login_required(login_url='/')
def salvar_permissoes(request):
    # print(request.POST)

    userId = request.POST['basicInput']
    escola_id = request.POST['escola']
    if escola_id == '0':
        escola_id = ''

    checkbox = ''
    try:
        ima = request.POST['ima']
        if checkbox != "":
            checkbox += ",ima"
        else:
            checkbox += "ima"
    except:
        pass

    try:
        ims = request.POST['ims']
        if checkbox != "":
            checkbox += ",ims"
        else:
            checkbox += "ims"
    except:
        pass

    try:
        opt = request.POST['opt']
        if checkbox != "":
            checkbox += ",opt"
        else:
            checkbox += "opt"
    except:
        pass

    try:
        cc = request.POST['cc']
        if checkbox != "":
            checkbox += ",cc"
        else:
            checkbox += "cc"
    except:
        pass

    try:
        ce = request.POST['ce']
        if checkbox != "":
            checkbox += ",ce"
        else:
            checkbox += "ce"
    except:
        pass

    try:
        dm = request.POST['dm']
        if checkbox != "":
            checkbox += ",dm"
        else:
            checkbox += "dm"
    except:
        pass

    try:
        ac = request.POST['ac']
        if checkbox != "":
            checkbox += ",ac"
        else:
            checkbox += "ac"
    except:
        pass

    try:
        vte = request.POST['vte']
        if checkbox != "":
            checkbox += ",vte"
        else:
            checkbox += "vte"
    except:
        pass

    try:
        sicge = request.POST['sicge']
        if checkbox != "":
            checkbox += ",sicge"
        else:
            checkbox += "sicge"
    except:
        pass

    try:
        sat = request.POST['sat']
        if checkbox != "":
            checkbox += ",sat"
        else:
            checkbox += "sat"
    except:
        pass

    try:
        gpu = request.POST['gpu']
        if checkbox != "":
            checkbox += ",gpu"
        else:
            checkbox += "gpu"
    except:
        pass

    try:
        ae = request.POST['ae']
        if checkbox != "":
            checkbox += ",ae"
        else:
            checkbox += "ae"
    except:
        pass

    user_is_perm = User_permission.objects.filter(user_id=userId).all()

    if user_is_perm:
        auth_user = User_permission.objects.get(user_id=userId)
        auth_user.permission = checkbox
        auth_user.escola_id = escola_id  # type: ignore
        auth_user.save()
        messages.success(request, 'Permissão realizada com sucesso!')
        return redirect('/permissoes-usuarios')

    else:
        auth_user = User_permission.objects.create(
            user_id=userId, permission=checkbox, escola_id=escola_id)
        messages.success(request, 'Permissão realizada com sucesso!')
        return redirect('/permissoes-usuarios')


@login_required(login_url='/')
def enviar_planejamento(request):

    user_id = getUserlogin(request)
    perm = User_permission.objects.filter(user_id=user_id).values()
    perm_escolas = perm[0]['escola_id']
    status_metas = Metas_efg.objects.filter(escola_id=perm_escolas).values()[0]
    all_metas = Metas_efg.objects.filter(escola_id=perm_escolas).values()

    if int(status_metas['situacao']) == 2 or int(status_metas['situacao']) == 3:
        messages.error(
            request, 'Não foi possível enviar o planejamento, o mesmo encontra-se aprovado ou está em status de análise!')
        return redirect('/cadastrar-metas')
    else:

        for metas in all_metas:

            idMetas = metas['id']
            atualiza_metas = Metas_efg.objects.get(id=idMetas)
            atualiza_metas.situacao = 2
            atualiza_metas.save()

        # escola_luiz_rassi = get_escolas(
        #     'where escola_id = 46 and situacao = 2')
        # escola_sara = get_escolas('where escola_id = 48 GROUP BY escola_id')
        # escola_bittencourt = get_escolas(
        #     'where escola_id = 54 GROUP BY escola_id')

        escola_luiz_rassi_1 = Metas_efg.objects.filter(
            escola_id=46, situacao=2).count()
        escola_luiz_rassi_2 = Metas_efg.objects.filter(
            escola_id=46, situacao=3).count()

        escola_sara_1 = Metas_efg.objects.filter(
            escola_id=48, situacao=2).count()
        escola_sara_2 = Metas_efg.objects.filter(
            escola_id=48, situacao=3).count()

        escola_bittencourt_1 = Metas_efg.objects.filter(
            escola_id=54, situacao=2).count()
        escola_bittencourt_2 = Metas_efg.objects.filter(
            escola_id=54, situacao=3).count()

        status_luiz_rassi = True if escola_luiz_rassi_1 + \
            escola_luiz_rassi_2 > 0 else False
        status_sara = True if escola_sara_1 + escola_sara_2 > 0 else False
        status_bittencourt = True if escola_bittencourt_1 + \
            escola_bittencourt_2 > 0 else False

        # print( escola_luiz_rassi,escola_sara,escola_bittencourt)
        if status_luiz_rassi == True and status_sara == True and status_bittencourt == True:
            sendPlan = getInstance(processName, "EnviarPlanejamentoTask")

            if sendPlan == True:
                messages.success(
                    request, 'Planejamento enviado com sucesso! Processo completado')
                return redirect('/cadastrar-metas')
            else:
                messages.error(
                    request, 'Não foi possível enviar o planejamento!')
                return redirect('/cadastrar-metas')
        else:
            messages.success(request, 'Planejamento enviado com sucesso!')
            return redirect('/cadastrar-metas')


@login_required(login_url='/')
def cadastrar_usuario(request):
    idSiga = request.POST['user_siga']
    idSele = request.POST['user_selecao']
    cpfUser = request.POST['cpf']
    users_sig = Users_ids.objects.filter(user_selecao_id=idSiga).all()
    users_sel = Users_ids.objects.filter(user_siga_id=idSele).all()

    if users_sig or users_sel:
        messages.error(
            request, 'Usuário siga ou usuário seleção já está cadastrado!')
        return redirect('/permissoes-usuarios')
    else:
        user = User.objects.create_user(
            username=request.POST['nome_user'],
            email=request.POST['email_user'],
            password=request.POST['senha_user'])

        id_user = User.objects.filter(username=user).values()

        auth_user = User_permission.objects.create(
            user_id=id_user[0]['id'], permission='', escola_id=None)

        users_ids = Users_ids.objects.create(
            user_id=id_user[0]['id'], user_selecao_id=idSele, user_siga_id=idSiga, cpf=cpfUser)
        messages.success(request, 'Usuário cadastrado com sucesso!')
        return redirect('/permissoes-usuarios')


def buscar_siga_selecao(request):
    cpf = request.GET.get('cpf')
    cpf = str(cpf).replace('.', '')
    cpf = cpf.replace('-', '')

    # print(cpf)
    # conexão com o banco de dados
    server = '200.137.215.60'
    database = 'DW_CETT'
    username = 'consulta'
    password = '6XGZxc2gdx14ygv'
    driver = '{ODBC Driver 17 for SQL Server}'

    # Conectando ao banco de dados
    conn = pyodbc.connect(
        f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}")
    cursor = conn.cursor()

    # Executando a consulta SQL

    query = "SELECT * FROM dbo.dUsuarios WHERE CPF = '" + str(cpf) + "'"
    cursor.execute(query)

    # Obtendo os resultados
    results = cursor.fetchall()
    # print(results)
    # print('resultados abaixo')
    # converter os resultados em um objeto JSONid

    json_results = [dict(zip(('SK_Usuario', 'NK_Usuario', 'NM_Login',
                         'NM_Usuario', 'NM_Sistema', 'CPF'), item)) for item in results]
    # print(json_results)
    # retornar a resposta em formato JSON
    return JsonResponse({'data': json_results})


@login_required(login_url='/')
def replanejar_curso(request):

    idCurso = request.POST['idCurso']
    turma = Metas_efg.objects.filter(id=int(idCurso)).values()
    tipo = turma[0]['tipo_curso_id']
    modalidade = turma[0]['modalidade_id']
    ano = turma[0]['ano']
    semestre = turma[0]['trimestre']
    carga_horaria_total = turma[0]['carga_horaria_total']

    saldo_disponivel = Saldo_replanejamento.objects.filter(
        modalidade_id=modalidade, tipo_id=tipo, ano=ano, semestre=semestre).values()
    if saldo_disponivel:
        idSaldo = saldo_disponivel[0]['id']
        saldoAntigo = saldo_disponivel[0]['saldo']
        change_value = Saldo_replanejamento.objects.get(id=idSaldo)
        change_value.saldo = int(carga_horaria_total) + int(saldoAntigo)
        change_value.save()
    else:
        insertValue = Saldo_replanejamento.objects.create(
            saldo=carga_horaria_total, modalidade_id=modalidade, tipo_id=tipo, ano=ano, semestre=semestre)

    # OBTÉM A TURMA ATUAL E ATUALIZA O STATUS PARA REPLANEJADO
    turmaReplanejada = Metas_efg.objects.get(id=int(idCurso))
    turmaReplanejada.situacao = 5
    turmaReplanejada.save()
    return redirect('/cadastrar-metas')


@login_required(login_url='/')
def buscar_saldo_replanejado(request):

    idOrigem = request.GET['idOrigem']
    turma = get_object_or_404(Metas_efg, id=idOrigem)
    tipo_curso_id = turma.tipo_curso_id
    modalidade_id = turma.modalidade_id
    saldo_especifico = get_object_or_404(
        Saldo_replanejamento, modalidade_id=modalidade_id, tipo_id=tipo_curso_id)
    return render(request, 'ajax/ajax_select_saldo_replanejado.html', {'saldo_especifico': saldo_especifico})
