from pydoc import describe
from unicodedata import category
from django.shortcuts import render, redirect
from appprojeto1.models import Cursos, Eixos, Item_apoiado, Metas_categoria, Metas_descricoes, Metas_efg, Metas_escolas, Metas_modalidade, Metas_sinteticas, Metas_trimestre, Orcamento_plano_trabalho, Rubrica, Solicitacao, Unidades
import json
from django.contrib import messages
import datetime
# Create your views here.
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

def view_eixos(request):
 #   data = {}
 #   data['db'] = Eixos.objects.all()
    eixos = Eixos.objects.all()
    cursos = []
    return render(request, 'form-element-input.html', {'eixos': eixos, 'cursos': cursos})


def load_funcoes(request):
    eixos_id = request.GET.get('id_eixos')
    curso = Cursos.objects.filter(id_eixos=eixos_id).all()
    return render(request, 'ajax_load_funcoes.html', {'qualificacoes': curso})


def view_index(request):
    return render(request, 'index.html')

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

def cadastrar_metas(request):
    metas = Metas_efg.objects.all()
    escolas = Metas_escolas.objects.all()
    capacitacao = Metas_categoria.objects.all()
    modalidade = Metas_modalidade.objects.all()
    trimestre = Metas_trimestre.objects.all()
    return render(request, 'cadastro_metas.html', {'metas': metas,
    'escolas':escolas,
    'categorias':capacitacao,
    'modalidades':modalidade,
    'trimestres':trimestre
    })

def cad_metas(request):
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
    vagas_turma =request.POST['vagas_turma']
    previsao_inicio = request.POST['data_p_inicio']
    previsao_fim = request.POST['data_p_fim']
    dias_semana = request.POST['dias_semana']
    previsao_abertura_edital = request.POST['p_abertura_edital']
    previsao_fechamento_edital = request.POST['p_fechamento_edital']
    data_registro = request.POST['escola']

    cadmetas = Metas_efg.objects.create(
        diretoria = diretoria,
        escola = escola,
        tipo_curso = tipo_curso,
        nome_curso = nome_curso,
        turno = turno,
        ano = ano,
        modalidade_oferta  = modalidade_oferta,
        trimestre = trimestre,
        carga_horaria = carga_horaria,
        vagas_totais = vagas_totais,
        vagas_turma = vagas_turma,
        carga_horaria_total = carga_horaria_total,
        previsao_inicio = previsao_inicio,
        previsao_fim = previsao_fim,
        dias_semana = dias_semana,
        previsao_abertura_edital = previsao_abertura_edital,
        previsao_fechamento_edital = previsao_fechamento_edital,
        data_registro = '2022-08-30',

    )

    messages.success(request,'Meta cadastrada com sucesso!')
    return redirect('/cadastrar-metas')

def apagar_meta(request):
    codigo = request.POST['id_deleta']
    meta = Metas_efg.objects.get(id=codigo)
    meta.delete()
    messages.success(request,'Meta removida com sucesso!')
    return redirect('/cadastrar-metas')

def editar_meta(request,codigo):
    meta_edit = Metas_efg.objects.get(id=codigo)
    return render(request, 'editar_metas.html', {'meta_edit': meta_edit})

def editarmetas(request):
    id_ = request.POST['id']
    diretoria = request.POST['basicInput']
    escola = request.POST['escola']
    tipo_curso = request.POST['tipo']
    nome_curso = request.POST['curso']
    turno = request.POST['turno']
    ano = request.POST['ano']
    modalidade_oferta =request.POST['modalidade']
    trimestre =request.POST['trimestre']
    carga_horaria = request.POST['carga_horaria']
    vagas_totais =request.POST['ch_total']
    vagas_turma =request.POST['vagas_totais']
    carga_horaria_total =request.POST['vagas_turma']
    previsao_inicio = request.POST['data_p_inicio']
    previsao_inicio = converter_data(previsao_inicio)
    previsao_fim = request.POST['data_p_fim']
    previsao_fim = converter_data(previsao_fim)
    dias_semana = request.POST['dias_semana']
    previsao_abertura_edital = request.POST['p_abertura_edital']
    previsao_abertura_edital = converter_data(previsao_abertura_edital)
    previsao_fechamento_edital = request.POST['p_fechamento_edital']
    previsao_fechamento_edital = converter_data(previsao_fechamento_edital)
    data_registro = str(datetime.datetime.now())
    data_registro = str(data_registro[:10])

    editmetas = Metas_efg.objects.get(id=id_)
    editmetas.diretoria = diretoria
    editmetas.escola = escola
    editmetas.tipo_curso = tipo_curso
    editmetas.nome_curso = nome_curso
    editmetas.turno = turno
    editmetas.ano = ano
    editmetas.modalidade_oferta = modalidade_oferta
    editmetas.trimestre = trimestre
    editmetas.carga_horaria = carga_horaria
    editmetas.carga_horaria_total = carga_horaria_total
    editmetas.vagas_totais = vagas_totais
    editmetas.vagas_turma = vagas_turma
    editmetas.previsao_inicio = previsao_inicio
    editmetas.previsao_fim = previsao_fim
    editmetas.dias_semana = dias_semana
    editmetas.previsao_abertura_edital = previsao_abertura_edital
    editmetas.previsao_fechamento_edital = previsao_fechamento_edital
    editmetas.data_registro = data_registro
    editmetas.save()
    messages.success(request,'Meta editada com sucesso!')
    return redirect('/cadastrar-metas')

def cadastrar_meta_sintetica(request):
    escolas = Metas_escolas.objects.all()
    capacitacao = Metas_categoria.objects.all()
    modalidade = Metas_modalidade.objects.all()
    trimestre = Metas_trimestre.objects.all()
    descricao = Metas_descricoes.objects.all()
    meta_sintetica = Metas_sinteticas.objects.all()
    return render(request,'cadastro_metas_sinteticas.html',{'meta_sinteticas':meta_sintetica,
    'escolas':escolas,
    'categorias':capacitacao,
    'modalidades':modalidade,
    'trimestres':trimestre,
    'descricoes':descricao})

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

    cadmetas = Metas_sinteticas.objects.create(diretoria=diretoria,escola=escola,ano=ano,modalidade=modalidade,categoria=tipo,descricao=descricao,ch_ofertada=ch_ofertada,vagas=vagas,repasse=repasse,valor_unitario=valor_unitario)

    messages.success(request,'Meta cadastrada com sucesso!')
    return redirect('/cadastrar-metas-sinteticas')

def apagar_meta_sintetica(request):
    codigo = request.POST['id_deleta']
    meta = Metas_sinteticas.objects.get(id=codigo)
    meta.delete()
    messages.success(request,'Meta removida com sucesso!')
    return redirect('/cadastrar-metas-sinteticas')

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
    editMetasS.escola = escola
    editMetasS.ano = ano
    editMetasS.modalidade = modalidade
    editMetasS.descricao = descricao
    editMetasS.categoria = tipo
    editMetasS.ch_ofertada = ch_ofertada
    editMetasS.vagas = vagas
    editMetasS.repasse = repasse
    editMetasS.valor_unitario = valor_unitario

    editMetasS.save()
    messages.success(request,'Meta editada com sucesso!')
    return redirect('/cadastrar-metas-sinteticas')

def orcamento_plano_trabalho(request):
    planejamento = Orcamento_plano_trabalho.objects.all()
    rubrica = Rubrica.objects.all()
    unidades = Unidades.objects.all()
    item_apoiado = Item_apoiado.objects.all()
    centro_custo = []
    return render(request, 'orcamento_plano_trabalho.html', {'rubricas': rubrica,'centro_custo':centro_custo,'unidades':unidades,'planejamentos':planejamento,'itens_apoiados':item_apoiado})

def rubrica(request):
    rubrica = Rubrica.objects.all()
    centro_custo = []
    return render(request, 'orcamento_plano_trabalho.html', {'rubricas': rubrica,'centro_custo':centro_custo})

def load_funcoes_rubrica(request):
    ia_id = request.GET.get('id_rubrica')
    item_apoiado = Item_apoiado.objects.filter(id_rubrica=ia_id).all()
    return render(request, 'ajax_load_item_apoiado.html', {'itens_apoiados': item_apoiado})

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
        rubrica = rubrica,
        item_apoiado = item_apoiado,
        und = und,
        qtd_global = qtd_global,
        valor_medio_unitario = valor_medio_unitario,
        valor_global = valor_global,
        custeio = custeio,
        capital = capital

    )
    messages.success(request,'Orçamento cadastrado com sucesso!')
    return redirect('/orcamento-plano-trabalho')

def apaga_orcamento(request):
    codigo = request.POST['id_deleta']
    meta = Orcamento_plano_trabalho.objects.get(id=codigo)
    meta.delete()
    messages.success(request,'Orçamento removido com sucesso!')
    return redirect('/orcamento-plano-trabalho')

def atualizar_orcamento(request):
    if request.POST['item_apoiado02'] != "Selecione um Item Apoiado":
        id_ = request.POST['idorc']
        receita = request.POST['tipo02']
        rubrica = request.POST['rubrica02']
        item_apoiado = request.POST['item_apoiado02']
        und = request.POST['unidade02']
        qtd_global = request.POST['qtd_global02']
        qtd_global = converter_casas(qtd_global)
        valor_medio_unitario = request.POST['v_m_unitario02']
        valor_medio_unitario = converter_casas(valor_medio_unitario)
        valor_global = request.POST['valor_global02']
        valor_global = converter_casas(valor_global)
        custeio = request.POST['custeio02']
        custeio = converter_casas(custeio)
        capital = request.POST['capital02']
        capital = converter_casas(capital)

        salvaorc = Orcamento_plano_trabalho.objects.get(id=id_)
        salvaorc.tipo = receita
        salvaorc.rubrica = rubrica
        salvaorc.item_apoiado = item_apoiado
        salvaorc.und = und
        salvaorc.qtd_global = qtd_global.replace(',','.')
        salvaorc.valor_medio_unitario = valor_medio_unitario.replace(',','.')
        salvaorc.valor_global = valor_global.replace(',','.')
        salvaorc.custeio = custeio.replace(',','.')
        salvaorc.capital = capital.replace(',','.')
        salvaorc.save()
        messages.success(request,'Orçamento alterado com sucesso!')
        return redirect('/orcamento-plano-trabalho')
    else:
        messages.error(request,'Por favor, selecione um item apoiado!')
        return redirect('/orcamento-plano-trabalho')
