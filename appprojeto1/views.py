from django.shortcuts import render, redirect
from appprojeto1.models import Cadastrar_curso,Udepi_municipio, Curso_escola, Cursos, Eixos, Item_apoiado, Metas_tipo, Metas_descricoes, Metas_efg, Metas_escolas, Metas_modalidade, Metas_sinteticas, Metas_trimestre, Orcamento_plano_trabalho, Rubrica, Solicitacao, Unidades
from DivisaoDeMetas.models import DivisaoDeMetasPorEscola
import json
from django.contrib import messages
import datetime
import MySQLdb
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
# EXECUTA LOCALMENTE
HOST="127.0.0.1"
USER="c35camundadb"	
PASS="iC7@hdDF"
DB="c35camundadb"
PORT=33306

#EXECUTA NO DOCKER
# HOST="isp.cett.dev.br"
# USER="c35camundadb"
# PASS="iC7@hdDF"
# DB="c35camundadb"
# PORT=3306

#FUNÇÃO PARA VERIFICAR IDS HORAS E VAGAS
#@login_required(login_url='/')
def select_vagas_horas(ano,trimestre,escola,modalidade,curso,tipo,type_count):
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
        query_start  = " AND"
    
    if trimestre:
        query += str(query_start) + " trimestre = '" + str(trimestre) + "'"
        query_start  = " AND"
    
    if escola:
        query += str(query_start) + " escola_id = '" + str(escola) + "'"
        query_start  = " AND"

    if modalidade:
        print(modalidade)
        query += str(query_start) + " modalidade_id = '" + str(modalidade) + "'"
        query_start  = " AND"

    if curso:
        query += str(query_start) + " curso_id = '" + str(curso) + "'"
        query_start  = " AND"

    if tipo:
        query += str(query_start) + " tipo_curso_id = '" + str(tipo) + "'"
        query_start  = " AND"
    


    print(query)
    # Executa o comando SQL
    c.execute(query)
 
    # Imprimir toda a primeira c�lula de todas as linhas

    for l in c.fetchall():
        vagas = str(l[0])
        print(vagas)
        if vagas == "None":
            vagas = "0"
        return vagas

#@login_required(login_url='/')
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
            escolas = (id,nome)
            escolas_siga.append({'id':id,'nome':nome})

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
        query = "SELECT nome from cursos where id = "+str(id_curso)+" GROUP BY nome"
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
            cursos_siga.append({'id':id,'nome':nome})

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
        front.append({'id':id_escola,'escola':nome_escola,'id_curso':id_curso,'curso':nome_curso,'status':status,'id_registro':id})
    print(front)
    return front


def converter_data(data):
    #14/03/2022
    data = str(data)
    dia = data[:2]
    mes = data[3:5]
    ano = data[6:]
    formato = ano + '-' + mes + '-' + dia
    return formato


def converter_casas(valor):
    valor = str(valor)
    valor = valor.replace(",",".")
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

    ch_total_geral = DivisaoDeMetasPorEscola.objects.filter(escola=escola,tipo=tipo_curso,ano=ano,modalidade=modalidade,semestre=semestre).all()
    try:
        chTotal = int(ch_total_geral.values()[0]['carga_horaria'])

    except:
        chTotal = 0
    return render(request, 'ajax/ajax_load_cht.html', {'ch_total_geral':chTotal })

def load_ch(request):
    escola = request.GET.get('escola_id')
    curso_selected = request.GET.get('curso_selected')
    tipocurso = request.GET.get('tipo_id')
    modalidade = request.GET.get('modalidade_id')
    eixo =  request.GET.get('eixo_id')
    print(str(escola)+'|'+str(curso_selected)+'|'+str(escola)+'|'+str(tipocurso)+'|'+str(modalidade)+'|'+str(eixo))
    carga_horaria = Cadastrar_curso.objects.filter(escola=escola,tipo=tipocurso,eixos=eixo,modalidade=modalidade,curso=curso_selected).all()
    print('>>>>>>>>>>>>>>>>>')
    print(carga_horaria.values())
    try:
        carga_horaria = int(carga_horaria.values()[0]['carga_horaria'])
        print(carga_horaria)
    except:
        carga_horaria = 0
    return render(request, 'ajax/ajax_load_carga_hr_curso.html', {'carga_hr':carga_horaria })

@login_required(login_url='/')
def load_cursos(request):
    escola_id = request.GET.get('escola_id')
    modalidade_id = request.GET.get('modalidade_id')
    id_tipo_curso = request.GET.get('tipo_id')
    eixos_id = request.GET.get('eixo_id')

    cursos = Cadastrar_curso.objects.filter(escola=escola_id,tipo=id_tipo_curso,modalidade=modalidade_id,eixos=eixos_id,status="ATIVO").all()

    return render(request, 'ajax/ajax_load_cursos.html', {'cursos': cursos})

@login_required(login_url='/')
def load_modalidade(request):
    escola_id = request.GET.get('escola_id')
    tipo_id = request.GET.get('tipo_id')
    eixos_id = request.GET.get('eixo_id')
    modalidade_id = request.GET.get('modalidade_id')
    cursos = Cadastrar_curso.objects.filter(escola=escola_id,tipo=tipo_id,eixos=eixos_id,modalidade=modalidade_id,status="ATIVO").all().values()

    return render(request, 'ajax/ajax_load_curso.html', {'cursos': cursos})

@login_required(login_url='/')
def load_eixos(request):
    escola_id = request.GET.get('escola_id')
    tipo_id = request.GET.get('tipo_id')
    eixos = Eixos.objects.filter(escola=escola_id,status="ATIVO").all()
    return render(request, 'ajax/ajax_load_eixos.html', {'eixos': eixos})

@login_required(login_url='/')
def load_municipios(request):
    id_escola = request.GET.get('escola_id')
    municipios = Udepi_municipio.objects.filter(escola_id=id_escola)
    return render(request, 'ajax/ajax_load_municipio.html', {'municipios': municipios})


@login_required(login_url='/')
def load_funcoes_filter(request):
    print(request)
    info = request.GET['filter_select']
    vagas = []
    results = Metas_efg.objects.raw('SELECT * FROM Turmas_planejado_orcado GROUP BY '+str(info))
   
    return render(request,'ajax/ajax_load_filter.html',{'results':results,'infos':info,'vagas':vagas})

@login_required(login_url='/')
def load_funcoes_vagas(request):
    print(request)
    ano = request.GET['ano']
    trimestre = request.GET['trimestre']
    escola = request.GET['escola']
    modalidade = request.GET['modalidade']
    curso = request.GET['curso']
    tipo = request.GET['tipo']
    #idEscola = select_vagas_horas('escola',subfilter)
    vagas = select_vagas_horas(ano,trimestre,escola,modalidade,curso,tipo,'vagas_totais')
    return render(request,'ajax/ajax_load_vagas.html',{'vagas':vagas})

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
    return render(request,'ajax/ajax_load_tbleixos.html',{'eixos':refresh_eixo})

@login_required(login_url='/')
def load_funcoes_gerencia_cursos(request):

    id = request.GET['id']
    status = request.GET['status']
    cursos = Cadastrar_curso.objects.select_related('escola').select_related('tipo').select_related('eixos').get(id=id)
    if status == "ATIVO":
        cursos.status = "INATIVO"
    else:
        cursos.status = "ATIVO"
    cursos.save()
    refresh_cursos = Cadastrar_curso.objects.select_related('escola').select_related('tipo').select_related('eixos').all()
    return render(request,'ajax/ajax_load_tblcursos.html',{'cursos':refresh_cursos})

@login_required(login_url='/')
def load_funcoes_rp(request):
    ano = request.GET['ano']
    trimestre = request.GET['trimestre']
    escola = request.GET['escola']
    modalidade = request.GET['modalidade']
    curso = request.GET['curso']
    tipo = request.GET['tipo']
    #idEscola = select_vagas_horas('escola',subfilter)
    total_horas = select_vagas_horas(ano,trimestre,escola,modalidade,curso,tipo,'carga_horaria_total')
    #vagas = select_vagas_horas(ano,trimestre,escola,modalidade,curso,tipo,'vagas_totais')
    #total_horas = int(horas) * int(vagas)

    if modalidade == "1":
        rp = float(total_horas) * 8.34

    elif modalidade == "2" or modalidade == "3":
        rp = float(total_horas) * 3.56
    else:
        rp = select_vagas_horas_gerais()
        print('Resultado do Recurso Planejado' + str(rp))

        
    return render(request,'ajax/ajax_load_recurso_planejado.html',{'rp':rp})

@login_required(login_url='/')
def load_funcoes_tabela(request):
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
        query_start  = " AND"
    
    if trimestre:
        query += str(query_start) + " trimestre = '" + str(trimestre) + "'"
        query_start  = " AND"
    
    if escola:
        query += str(query_start) + " escola = '" + str(escola) + "'"
        query_start  = " AND"

    if modalidade:
        query += str(query_start) + " modalidade_id = '" + str(modalidade) + "'"
        query_start  = " AND"

    if curso:
        query += str(query_start) + " curso_id = '" + str(curso) + "'"
        query_start  = " AND"

    if tipo:
        query += str(query_start) + " tipo_curso_id = '" + str(tipo) + "'"
        query_start  = " AND"
    

    info = Metas_efg.objects.raw(query)
    return render(request,'ajax/ajax_load_table.html',{'filtros':info})

@login_required(login_url='/')
def load_funcoes_total_horas(request):
    ano = request.GET['ano']
    trimestre = request.GET['trimestre']
    escola = request.GET['escola']
    modalidade = request.GET['modalidade']
    curso = request.GET['curso']
    tipo = request.GET['tipo']
    total_horas = select_vagas_horas(ano,trimestre,escola,modalidade,curso,tipo,'carga_horaria_total')
    
    #vagas = select_vagas_horas(ano,trimestre,escola,modalidade,curso,tipo,'vagas_totais')
    #total_horas = int(horas) * int(vagas)
    return render(request,'ajax/ajax_load_total_horas.html',{'total_horas':total_horas})

def view_geral(request):
    return render(request, 'login.html')

@csrf_protect
def Autenticar(request):
    #return render(request,"forms.html")
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
    return render(request, 'index.html')

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
    print(eixo)
    submit = Solicitacao.objects.create(
        eixo=neweixo, curso=newcurso, modalidade=modalidade, tipo=tipo, justificativa=justificativa)
    return redirect('/eixos')

@login_required(login_url='/')
def cadastrar_metas(request):
    tipo_curso = Metas_tipo.objects.all()
    escolas_cad = Metas_escolas.objects.filter(tipo=0)
    modalidade = Metas_modalidade.objects.all()
    lancamentos = Metas_efg.objects.all()
    municipios = Udepi_municipio.objects.filter(escola_id=39)
    anos = Metas_efg.objects.raw("Select id,ano from Turmas_planejado_orcado GROUP BY ano")
    mod = Metas_efg.objects.raw("Select id,modalidade_id from Turmas_planejado_orcado GROUP BY modalidade_id")
    trimestre = Metas_efg.objects.raw("Select id,trimestre from Turmas_planejado_orcado GROUP BY trimestre")
    escolas = Metas_efg.objects.raw("Select id,escola_id from Turmas_planejado_orcado GROUP BY escola_id")
    cursos_cad = Metas_efg.objects.raw("Select id,curso_id from Turmas_planejado_orcado GROUP BY curso_id")
    tipos_cad = Metas_efg.objects.raw("Select id,tipo_curso_id from Turmas_planejado_orcado GROUP BY tipo_curso_id")
    eixos = Eixos.objects.filter(escola=39)
    cursos =  Cadastrar_curso.objects.filter(escola=39,tipo=0,modalidade=1,eixos=17,status="ATIVO").all()

    return render(request, 'cadastro_metas.html',{"tipos":tipo_curso,
    'escolas':escolas_cad,
    'modalidades':modalidade,
    'lancamentos':lancamentos,
    'anos':anos,
    'mods':mod,
    'trimestres':trimestre,
    'escolas_cad':escolas,
    'cursos_cad':cursos_cad,
    'tipos_cad':tipos_cad,
    'eixos':eixos,
    'cursos':cursos,
    'municipios':municipios})

@login_required(login_url='/')
def cad_metas(request):
    print(request.POST)
    diretoria = request.POST['basicInput']
    escola = request.POST['escola']
    tipo_curso = request.POST['tipo']
    nome_curso = request.POST['curso']
    turno = request.POST['turno']
    ano = request.POST['ano']
    modalidade_oferta =request.POST['modalidade']
    trimestre =request.POST['trimestre']
    carga_horaria = request.POST['carga_horaria']
    carga_horaria_total =request.POST['ch_total']
    vagas_totais =request.POST['vagas_totais']
    previsao_inicio = request.POST['data_p_inicio']
    previsao_fim = request.POST['data_p_fim']
    dias_semana = request.POST['dias_semana']
    if request.POST['p_abertura_edital'] != "" and request.POST['p_fechamento_edital'] != "":
        previsao_abertura_edital = request.POST['p_abertura_edital']
        previsao_fechamento_edital = request.POST['p_fechamento_edital']
    eixos = request.POST['eixo']
    udepi = request.POST['municipio']

    meta_is_exist = Metas_efg.objects.filter(escola_id=escola,tipo_curso_id=tipo_curso,modalidade_id=modalidade_oferta,ano=ano,trimestre=trimestre,udepi=udepi).values()
    print('-------------------------------------------------------\n\n\n\n'+ str(meta_is_exist))
    if meta_is_exist:
        messages.error(request,'): Desculpe, mas já existe uma meta adicionada com estes dados!')
        return redirect('/cadastrar-metas')
    else:
        if request.POST['p_abertura_edital'] != "" and request.POST['p_fechamento_edital'] != "":
            cadmetas = Metas_efg.objects.create(
                diretoria = diretoria,
                escola_id = escola,
                tipo_curso_id = tipo_curso,
                curso_id = nome_curso,
                turno = turno,
                ano = ano,
                eixo_id = eixos,
                modalidade_id  = modalidade_oferta,
                trimestre = trimestre,
                carga_horaria = carga_horaria,
                vagas_totais = vagas_totais,
                carga_horaria_total = carga_horaria_total,
                previsao_inicio = previsao_inicio,
                previsao_fim = previsao_fim,
                dias_semana = dias_semana,
                previsao_abertura_edital = previsao_abertura_edital,
                previsao_fechamento_edital = previsao_fechamento_edital,
                jus_reprovacao = '',
                udepi_id = udepi
                )
        else:
            cadmetas = Metas_efg.objects.create(
                diretoria = diretoria,
                escola_id = escola,
                tipo_curso_id = tipo_curso,
                curso_id = nome_curso,
                turno = turno,
                ano = ano,
                eixo_id = eixos,
                modalidade_id  = modalidade_oferta,
                trimestre = trimestre,
                carga_horaria = carga_horaria,
                vagas_totais = vagas_totais,
                carga_horaria_total = carga_horaria_total,
                previsao_inicio = previsao_inicio,
                previsao_fim = previsao_fim,
                dias_semana = dias_semana,
                jus_reprovacao = '',
                udepi_id = udepi
                )

        atualiza_saldo = DivisaoDeMetasPorEscola.objects.filter(escola=escola,tipo=tipo_curso,ano=ano).values()
        id_filtro = atualiza_saldo[0]['id']
        novo_saldo = int(atualiza_saldo[0]['carga_horaria']) - int(carga_horaria_total)
        atualiza_divisao = DivisaoDeMetasPorEscola.objects.get(id=id_filtro)
        atualiza_divisao.carga_horaria = novo_saldo
        atualiza_divisao.save()
        messages.success(request,'Meta cadastrada com sucesso!')
        return redirect('/cadastrar-metas')
    
@login_required(login_url='/')
def apagar_meta(request):
    codigo = request.POST['id_deleta']
    escola = request.POST['escola_delete']
    tipo_curso = request.POST['tipo_delete']
    ano = request.POST['ano_delete']
    carga_horaria_total = request.POST['cht']
    meta = Metas_efg.objects.get(id=codigo)
    meta.delete()

    atualiza_saldo = DivisaoDeMetasPorEscola.objects.filter(escola=escola,tipo=tipo_curso,ano=ano).values()
    id_filtro = atualiza_saldo[0]['id']
    novo_saldo = int(atualiza_saldo[0]['carga_horaria']) + int(carga_horaria_total)
    atualiza_divisao = DivisaoDeMetasPorEscola.objects.get(id=id_filtro)
    atualiza_divisao.carga_horaria = novo_saldo
    atualiza_divisao.save()
    messages.success(request,'Meta removida com sucesso!')
    return redirect('/cadastrar-metas')

@login_required(login_url='/')
def editar_meta(request,codigo):
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
    pi = datetime.datetime.strftime(pi,'%Y-%m-%d')
    pf = pega_eixos[0]['previsao_fim']
    pf = datetime.datetime.strftime(pf,'%Y-%m-%d')
    dia_semana = pega_eixos[0]['dias_semana']
    idEdit = pega_eixos[0]['id']
    
    
    tipos_cursos = Metas_tipo.objects.all()
    
    escolas = Metas_escolas.objects.filter(tipo=0)
    eixos = Eixos.objects.filter(escola_id=idEscola)
    modalidades = Metas_modalidade.objects.all()
    municipios = Udepi_municipio.objects.filter(escola_id=idEscola)

    cursos = Cadastrar_curso.objects.filter(eixos=idEixos,tipo_id=tipoCursos)
    atualiza_saldo = DivisaoDeMetasPorEscola.objects.filter(escola=infoFiltro[0]['escola_id'],tipo=infoFiltro[0]['tipo_curso_id'],ano=infoFiltro[0]['ano']).values()
    id_filtro = atualiza_saldo[0]['id']
    limite = atualiza_saldo[0]['carga_horaria']
    return render(request, 'editar_metas.html', {'meta_edit': meta_edit,
    'tipos_cursos':tipos_cursos,
    'modalidades':modalidades,
    'escolas':escolas,
    'eixos':eixos,
    'cursos':cursos,
    'limite':limite,
    'municipios':municipios,
    'diretoria':diretoria,
    'idEscola':idEscola,
    'idMunicipio':idMunicipio,
    'tipoCursos':tipoCursos,
    'idEixos':idEixos,
    'idModalidade':idModalidade,
    'idCurso':idCurso,
    'turno':turno,
    'ano':ano,
    'trimestre':trimestre,
    'ch':ch,
    'qtdVagas':qtdVagas,
    'cht':cht,
    'pi':pi,
    'pf':pf,
    'dia_semana':dia_semana,
    'idEdit':idEdit})

@login_required(login_url='/')
def editarmetas(request):
    
    id_ = request.POST['id']
    diretoria = request.POST['diretoria']
    escola = request.POST['escola']
    municipio = request.POST['municipio']
    print(municipio)
    tipo_curso = request.POST['tipo']
    eixos = request.POST['eixo']
    modalidade_oferta =request.POST['modalidade']
    nome_curso = request.POST['curso']
    turno = request.POST['turno']
    ano = request.POST['ano']
    trimestre =request.POST['trimestre']
    carga_horaria = request.POST['carga_horaria']
    vagas_totais =request.POST['vagas_totais']
    carga_horaria_total = request.POST['ch_total']
    previsao_inicio = request.POST['data_p_inicio']
    #previsao_inicio = converter_data(previsao_inicio)
    previsao_fim = request.POST['data_p_fim']
    #previsao_fim = converter_data(previsao_fim)
    dias_semana = request.POST['dias_semana']

    editmetas = Metas_efg.objects.get(id=id_)
    editmetas.udepi_id = municipio
    editmetas.diretoria = diretoria
    editmetas.escola_id = escola
    editmetas.tipo_curso_id = tipo_curso
    editmetas.eixo_id = eixos
    editmetas.curso_id = nome_curso
    editmetas.turno = turno
    editmetas.ano = ano
    editmetas.modalidade_id = modalidade_oferta
    editmetas.trimestre = trimestre
    editmetas.carga_horaria = carga_horaria
    editmetas.carga_horaria_total = carga_horaria_total
    editmetas.vagas_totais = vagas_totais
    editmetas.previsao_inicio = previsao_inicio
    editmetas.previsao_fim = previsao_fim
    editmetas.dias_semana = dias_semana
    editmetas.save()

    atualiza_saldo = DivisaoDeMetasPorEscola.objects.filter(escola=escola,tipo=tipo_curso,ano=ano).values()
    id_filtro = atualiza_saldo[0]['id']
    saldo_atual = int(atualiza_saldo[0]['carga_horaria'])
    cht_antiga = int(request.POST['carga_horaria'])
    cht_atual = int(request.POST['ch_total'])
    if cht_atual < cht_antiga:
        saldo = saldo_atual + (cht_antiga - cht_atual)
    elif cht_atual > cht_antiga:
        saldo = saldo_atual - (cht_atual - cht_antiga)
    else:
        saldo = saldo_atual
    
    atualiza_saldo = DivisaoDeMetasPorEscola.objects.get(id=id_filtro)
    #atualiza_saldo.created_at = datetime.datetime.now()
    atualiza_saldo.carga_horaria = saldo
    atualiza_saldo.save()

    messages.success(request,'Meta editada com sucesso!')
    return redirect('/cadastrar-metas')

@login_required(login_url='/')
def cadastrar_meta_sintetica(request):
    escolas = Metas_escolas.objects.filter(tipo=0)
    tipo_curso = Metas_tipo.objects.all()
    modalidade = Metas_modalidade.objects.all()
    trimestre = Metas_trimestre.objects.all()
    descricao = Metas_descricoes.objects.all()
    meta_sintetica = Metas_sinteticas.objects.select_related('escola').select_related('modalidade').select_related('categoria').all().order_by('ano')
    eixos = Eixos.objects.all()
    return render(request,'cadastro_metas_sinteticas.html',{'meta_sinteticas':meta_sintetica,
    'escolas':escolas,
    'tipos_curso':tipo_curso,
    'modalidades':modalidade,
    'trimestres':trimestre,
    'descricoes':descricao,
    'eixos':eixos})

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

    messages.success(request,'Meta cadastrada com sucesso!')
    return redirect('/cadastrar-metas-sinteticas')

@login_required(login_url='/')
def apagar_meta_sintetica(request):
    codigo = request.POST['id_deleta']
    meta = Metas_sinteticas.objects.get(id=codigo)
    meta.delete()
    messages.success(request,'Meta removida com sucesso!')
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
    editMetasS.escola_id = escola
    editMetasS.ano = ano
    editMetasS.modalidade_id = modalidade
    editMetasS.descricao_id = descricao
    editMetasS.tipo_id = tipo
    editMetasS.ch_ofertada = ch_ofertada
    editMetasS.vagas = vagas
    editMetasS.repasse = repasse
    editMetasS.valor_unitario = valor_unitario

    editMetasS.save()
    messages.success(request,'Meta editada com sucesso!')
    return redirect('/cadastrar-metas-sinteticas')

@login_required(login_url='/')
def orcamento_plano_trabalho(request):
    planejamento = Orcamento_plano_trabalho.objects.all()
    rubrica = Rubrica.objects.all()
    unidades = Unidades.objects.all()
    item_apoiado = Item_apoiado.objects.all()
    centro_custo = []
    return render(request, 'orcamento_plano_trabalho.html', {'rubricas': rubrica,'centro_custo':centro_custo,'unidades':unidades,'planejamentos':planejamento,'itens_apoiados':item_apoiado})

@login_required(login_url='/')
def rubrica(request):
    rubrica = Rubrica.objects.all()
    centro_custo = []
    return render(request, 'orcamento_plano_trabalho.html', {'rubricas': rubrica,'centro_custo':centro_custo})

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
        tipo = receita,
        rubrica_id = rubrica,
        item_apoiado_id = item_apoiado,
        und = und,
        qtd_global = qtd_global,
        valor_medio_unitario = valor_medio_unitario,
        valor_global = valor_global,
        custeio = custeio,
        capital = capital

    )
    messages.success(request,'Orçamento cadastrado com sucesso!')
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
    custeio =request.POST['custeio2']
    capital =request.POST['capital2']
    

    editorcamento = Orcamento_plano_trabalho.objects.get(id=id_)
    editorcamento.tipo = tipo
    editorcamento.rubrica_id = rubrica
    editorcamento.item_apoiado_id = item_apoiado
    editorcamento.und = unidade
    editorcamento.qtd_global = qtd_global
    editorcamento.valor_medio_unitario = v_m_unitario
    editorcamento.valor_global = valor_global
    editorcamento.custeio = custeio
    editorcamento.capital = capital
    editorcamento.save()
    messages.success(request,'Orçamento editado com sucesso!')
    return redirect('/orcamento-plano-trabalho')

@login_required(login_url='/')
def apaga_orcamento(request):
    codigo = request.POST['id_deleta']
    meta = Orcamento_plano_trabalho.objects.get(id=codigo)
    meta.delete()
    messages.success(request,'Orçamento removido com sucesso!')
    return redirect('/orcamento-plano-trabalho')

@login_required(login_url='/')
def cadastro_curso_escola(request):
    escolas = Metas_escolas.objects.filter(tipo=0)
    curso = Cadastrar_curso.objects.all()
    return render(request, 'cadastro_curso_escola.html', {'escolas': escolas,'cursos':curso})

@login_required(login_url='/')
def cad_curso_escola(request):
    escola = request.POST['escola']
    curso = request.POST['curso']
    status = request.POST['status']

    cadmetas = Curso_escola.objects.create(escola_id=escola,curso_id=curso,status=status)

    messages.success(request,'Curso cadastrado na escola selecionada!')
    return redirect('/cadastrar-curso-escola')

@login_required(login_url='/')
def apagar_curso_escola(request):
    codigo = request.POST['id_deleta']
    curso = Curso_escola.objects.get(id=codigo)
    print(curso)
    curso.delete()
    messages.success(request,'Curso removido desta escola!')
    return redirect('/cadastrar-curso-escola')

@login_required(login_url='/')
def editar_curso_escola(request):
    id_ = request.POST['id_edit']
    print(id_)
    escola_id = request.POST['escola_modal']
    curso_id = request.POST['curso_modal']
    status = request.POST['status_modal']
    editCursoEscola = Curso_escola.objects.get(id=id_)
    editCursoEscola.escola_id = escola_id
    editCursoEscola.curso_id = curso_id
    editCursoEscola.status = status
    
    editCursoEscola.save()
    messages.success(request,'Registros alterados com sucesso!')
    return redirect('/cadastrar-curso-escola')

@login_required(login_url='/')
def cadastrar_curso(request):
    cursos = Cadastrar_curso.objects.select_related('escola').select_related('tipo').select_related('eixos').all()
    tipos = Metas_tipo.objects.all()
    eixos = Eixos.objects.all()
    escolas_cursos = Cadastrar_curso.objects.raw('Select * from cursos group by escola_id')
    tipo_cursos = Cadastrar_curso.objects.raw('Select * from cursos group by tipo_id')
    eixos_curso = Cadastrar_curso.objects.raw('Select * from cursos group by eixos_id')
    modalidade = Metas_modalidade.objects.all()
    escolas = Metas_escolas.objects.filter(tipo=0)
    eixos_inicial = Eixos.objects.filter(escola_id=39)
    return render(request,'cadastro_curso.html',{"cursos":cursos,'tipos':tipos,'eixos':eixos,'escolas_cursos':escolas_cursos,'tipo_curso':tipo_cursos,'eixos_curso':eixos_curso,'eixos_inicial':eixos_inicial,'modalidades':modalidade,'escolas':escolas})

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
    cadCurso = Cadastrar_curso.objects.create(escola_id=escola,tipo_id=tipo,eixos_id=eixos,curso=curso,status=status,modalidade_id=modalidade,escolaridade=escolaridade,carga_horaria=carga_horaria,idade_min=idade_minima)

    messages.success(request,'Curso cadastrado!')
    return redirect('/cadastrar-curso')

@login_required(login_url='/')
def del_curso(request):
    codigo = request.POST['id_deleta']
    curso = Cadastrar_curso.objects.get(id=codigo)
    print(curso)
    curso.delete()
    messages.success(request,'Curso removido desta escola!')
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
    editaCurso = Cadastrar_curso.objects.get(id=id_)
    editaCurso.escola_id = escola
    editaCurso.tipo_id = tipo
    editaCurso.escolaridade = escolaridade
    editaCurso.idade_min = idade_min
    editaCurso.eixos_id = eixos
    editaCurso.curso = curso
    editaCurso.carga_horaria = carga_horaria
    editaCurso.status = status
    editaCurso.save()
    messages.success(request,'Registros alterados com sucesso!')
    return redirect('/cadastrar-curso')

@login_required(login_url='/')
def cadastrar_udepi(request):
    escolas = Metas_escolas.objects.filter(tipo=0)
    udepis = Udepi_municipio.objects.all()
    return render(request,'cadastrar_udepi.html',{'escolas':escolas,'udepis':udepis})