from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from appprojeto1.models import Edital
from appprojeto1.models import User, User_permission, Edital, Users_ids
from appprojeto1.models import Metas_efg, Metas_escolas, Metas_tipo, Metas_modalidade, Eixos, Cadastrar_curso
from retificacao_edital.models import Editais_Retificados, Turmas_Retificadas
from django.http import JsonResponse
from django.db import transaction


def getUserlogin(request):
    username = request.user
    id_user = User.objects.filter(username=username).values()
    return id_user[0]['id']


def get_permission(request):
    user_id = getUserlogin(request)
    perm = User_permission.objects.filter(user_id=user_id).values()
    return perm[0]

# Create your views here.


@login_required(login_url='/')
def retificar_edital(request):

    editais = metas = Edital.objects.raw("Select DISTINCT * from Turmas_planejado_orcado INNER JOIN edital_ensino ON Turmas_planejado_orcado.num_edital_id = edital_ensino.id INNER JOIN tipo_curso ON Turmas_planejado_orcado.tipo_curso_id = tipo_curso.id INNER JOIN modalidade ON Turmas_planejado_orcado.modalidade_id = modalidade.id where dt_ini_edit is not NULL and status= 0  group by Turmas_planejado_orcado.num_edital_id")
    escolas = Metas_escolas.objects.filter(tipo=0).all()
    tipo_curso = Metas_tipo.objects.all()
    modalidade = Metas_modalidade.objects.all()
    eixos = Eixos.objects.filter(escola=39)
    cursos = Cadastrar_curso.objects.filter(
        escola=39, tipo=0, modalidade=1, eixos=17, status="ATIVO").all()
    return render(request, 'retificacao_edital.html', {'permissoes': get_permission(request), 'editais': editais, 'escolas': escolas, 'tipos': tipo_curso, 'modalidades': modalidade, 'eixos': eixos, 'cursos': cursos})


@login_required(login_url='/')
def load_turmas_edital(request):

    editalId = request.GET['editalId']
    turmas = Metas_efg.objects.filter(num_edital_id=editalId).all()
    turmas_retificadas = Turmas_Retificadas.objects.filter(
        num_edital_id=editalId)
    return render(request, 'ajax/ajax_tbl_retificacao.html', {'editais': turmas, 'turmas_retificadas': turmas_retificadas})


@login_required(login_url='/')
def load_turmas_retificadas(request):
    editalId = request.GET['editalId']
    turmas_retificadas = Editais_Retificados.objects.filter(
        edital_origem_id=editalId).first()
    editalRetificado = turmas_retificadas.id
    turmas_retificadas = Turmas_Retificadas.objects.filter(
        num_edital_id=editalRetificado)
    return render(request, 'ajax/ajax_tbl_turmas_retificadas.html', {'turmas_retificadas': turmas_retificadas})


@login_required(login_url='/')
def load_turmas_edital_retificacao(request):

    editalId = request.GET['edital_id']
    turmas = Metas_efg.objects.filter(num_edital_id=editalId).all()

    return render(request, 'ajax/turmas_edital_retificacao.html', {'editais': turmas})


@login_required(login_url='/')
def load_edital_exist(request):

    editalId = request.GET['edital_id']
    editais_retificados = Editais_Retificados.objects.filter(
        edital_origem_id=editalId).first()
    if editais_retificados:
        saldo_disponivel = editais_retificados.saldo_disponivel
    else:
        saldo_disponivel = None
    return JsonResponse({'saldo_disponivel': saldo_disponivel})


@login_required(login_url='/')
def retifica_turma_edital(request):
    print(request.POST)
    with transaction.atomic():
        # CRIA O EDITAL
        edital_id = request.POST['editalOrigem']
        edital_ano = request.POST['ano_edital']
        edital_data_inicial_edital = request.POST['data_inicial_edital']
        edital_data_fim_edital = request.POST['data_fim_edital']
        edital_data_ini_inscricao = request.POST['data_ini_inscricao']
        edital_data_fim_inscricao = request.POST['data_fim_inscricao']
        saldo_restante = request.POST['saldo_restante']

        diretoria = request.POST['basicInput']
        escola = request.POST['escola_id_modal']
        tipo_curso = request.POST['tipo']
        curso = request.POST['curso']
        turno = request.POST['turno']
        ano = request.POST['ano']
        modalidade = request.POST['modalidade']
        trimestre = request.POST['trimestre']
        vagas_totais = request.POST['vagas_totais']
        carga_horaria = request.POST['carga_horaria']
        carga_horaria_total = request.POST['ch_total']
        previsao_inicio = request.POST['data_p_inicio']
        previsao_fim = request.POST['data_p_fim']
        dias_semana = request.POST['dias_semana']
        eixo = request.POST['eixo']
        udepi = request.POST['municiopio_id_modal']
        curso_tecnico = request.POST['curso_tecnico']
        qualificacoes = request.POST['qualificacoes']
        origem_replan = request.POST['origem_retificacao']

        # VERIFICA SE O EDITAL JA EXISTE
        edital = Editais_Retificados.objects.filter(
            edital_origem_id=edital_id).first()
        if edital:
            edital.saldo_disponivel = saldo_restante
            edital.save()
        else:
            prox_edital = Edital.objects.raw(
                f"""
                    SELECT COALESCE(MAX(num_edital) + 1, 1) AS prox_edital
                    FROM (
                    SELECT
                        num_edital, ano
                    FROM edital_ensino UNION ALL
                    SELECT
                        num_edital, ano
                    FROM editais_retificados
                    ) tb
                    WHERE ano = {edital_ano} AND escola_id = {escola}
                """.format(edital_ano, escola))[0].prox_edital

            edital = Editais_Retificados.objects.create(
                num_edital=prox_edital,
                ano=edital_ano,
                dt_ini_edit=edital_data_inicial_edital,
                dt_fim_edit=edital_data_fim_edital,
                dt_ini_insc=edital_data_ini_inscricao,
                dt_fim_insc=edital_data_fim_inscricao,
                escola_id=escola,
                edital_origem_id=edital_id,
                saldo_disponivel=saldo_restante,
                satus=0
            )

        turma = Turmas_Retificadas.objects.create(
            num_edital_id=edital.id,
            diretoria=diretoria,
            escola_id=escola,
            tipo_curso_id=tipo_curso,
            curso_id=curso,
            turno=turno,
            ano=ano,
            modalidade_id=modalidade,
            trimestre=trimestre,
            vagas_totais=vagas_totais,
            carga_horaria=carga_horaria,
            carga_horaria_total=carga_horaria_total,
            previsao_inicio=previsao_inicio,
            previsao_fim=previsao_fim,
            dias_semana=dias_semana,
            eixo_id=eixo,
            udepi_id=udepi,
            curso_tecnico=curso_tecnico,
            qualificacoes=qualificacoes,
            origem_replan_id=origem_replan
        )
    return JsonResponse({"success_message": "Solicitação Realizada!"})


@login_required(login_url='/')
def redefinir_retificacao(request):
    with transaction.atomic():
        editalId = request.GET['editalId']

        # PEGA O EDITAL QUE PERTENCE AO ID
        edital = Editais_Retificados.objects.filter(
            edital_origem_id=editalId).first()

        # obtenho turmas relacionada a este edital
        turmas = Turmas_Retificadas.objects.filter(
            num_edital_id=edital.id).all()
        turmas.delete()

        # remove o edital
        edital = Editais_Retificados.objects.filter(id=edital.id)
        edital.delete()

        return JsonResponse({"success_message": "Solicitação Realizada!"})


@login_required(login_url='/')
def remover_turma_retificada(request):
    with transaction.atomic():
        turma_id = request.GET['turma_id']
        turma = Turmas_Retificadas.objects.get(id=turma_id)
        edital_id = turma.num_edital_id
        saldo_devolver = turma.carga_horaria_total
        turma.delete()

        edital = Editais_Retificados.objects.get(id=edital_id)
        saldo_atual = edital.saldo_disponivel
        novo_saldo = saldo_atual + saldo_devolver
        edital.saldo_disponivel = novo_saldo
        edital.save()
        return JsonResponse({"success_message": "Solicitação Realizada!"})


@login_required(login_url='/')
def verifica_saldo_disponivel(request):

    editalId = request.GET['edital_id']
    editais_retificados = Editais_Retificados.objects.filter(
        edital_origem_id=editalId).first()
    saldo_disponivel = editais_retificados.saldo_disponivel
    return JsonResponse({'saldo_disponivel': saldo_disponivel})


@login_required(login_url='/')
def enviar_edital_aprovacao(request):
    with transaction.atomic():
        turma_id = request.GET['edital_id']
        edital_retificado = Editais_Retificados.objects.filter(
            edital_origem_id=turma_id).first()
        edital_retificado.status = 0
        edital_retificado.save()

        Turmas_Retificadas.objects.filter(
            num_edital_id=edital_retificado.id).update(situacao=2)

        return JsonResponse({"success_message": "Solicitação Realizada!"})
