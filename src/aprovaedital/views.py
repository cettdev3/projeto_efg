from django.shortcuts import render, redirect
from appprojeto1.models import User, User_permission,Edital,Users_ids
from retificacao_edital.models import Editais_Retificados
from django.contrib import messages
from django.db.models import Q
from requests.auth import HTTPBasicAuth
import requests as req
import json
import envconfiguration as config

#host = config.CAMUNDA_URL #type:ignore
host = 'https://processos.cett.dev.br/engine-rest/'
processName = "ElaborarEdital"
autentication = HTTPBasicAuth('dmartins', 'CETT@2022')


def camundaPutVariable(taskId,variable,variableValue,type):
    #https://processos.cett.dev.br/engine-rest/task/bd7fa2eb-8536-11ed-ad45-0242ac130024/variables/alteracao
    headers = {'Content-type': 'application/json'}
    bodyJson = {"value" : variableValue, "type": type}
    putVariable = req.put(f"{host}/task/{taskId}/variables/{variable}",json=bodyJson, auth=autentication, headers=headers)
    return True if putVariable.status_code == 204 else  False

def getInstance(processName, taskDefinition,request):
    #PEGA O ID DO USUÁRIO LOGADO
    userLogged = getUserlogin(request)

    #PEGA O ID DO SELEÇÃO e SIGA DO USUÁRIO LOGADO
    infoUserLogged = Users_ids.objects.filter(user_id = userLogged).values()
    idUserSelecao = infoUserLogged[0]['user_selecao_id']
    idUserSiga = infoUserLogged[0]['user_siga_id']

    taskDefinitionKey = taskDefinition
    url = f"{host}/task?processDefinitionKey={processName}"
    requisicao = req.get(url, json={}, auth=autentication)
    retorno = requisicao.text
    json_object = json.loads(retorno)
    print(json_object)
    for dados in json_object:
        print(dados)
        try:
            if dados['taskDefinitionKey'] == taskDefinitionKey:
                idTask = dados['id']
                headers = {'Content-type': 'application/json'}
                putvariable = camundaPutVariable(idTask,'alteracao','não','String')
                putUserLogin = camundaPutVariable(idTask,'UserDjangoAuth',userLogged,'String')
                putUserSelecao = camundaPutVariable(idTask,'UserSelecaoAuth',idUserSelecao,'String')
                putUserSiga = camundaPutVariable(idTask,'UserSigaAuth',idUserSiga,'String')

                if putvariable == True and putUserSelecao == True and putUserLogin == True and putUserSiga == True:
                    completeTask = req.post(
                        f"{host}/task/{idTask}/complete", auth=autentication, headers=headers)
                    if completeTask.status_code == 204:
                        print('Taks is completed!')
                        return True
                    else:
                        return False
                else:
                    return False
        except:
            if dados[0]['taskDefinitionKey'] == taskDefinitionKey:
                idTask = dados['id']
                headers = {'Content-type': 'application/json'}
                putvariable = camundaPutVariable(idTask,'alteracao','não','String')
                putUserLogin = camundaPutVariable(idTask,'UserDjangoAuth',userLogged,'String')
                putUserSelecao = camundaPutVariable(idTask,'UserSelecaoAuth',idUserSelecao,'String')
                putUserSiga = camundaPutVariable(idTask,'UserSigaAuth',idUserSiga,'String')

                if putvariable == True and putUserSelecao == True and putUserLogin == True and putUserSiga == True:
                    completeTask = req.post(
                        f"{host}/task/{idTask}/complete", auth=autentication, headers=headers)
                    if completeTask.status_code == 204:
                        print('Taks is completed!')
                        return True
                    else:
                        return False
                else:
                    return False

def getUserlogin(request):
    username = request.user
    id_user = User.objects.filter(username=username).values()
    return id_user[0]['id']

def get_permission(request):
    user_id = getUserlogin(request)
    perm = User_permission.objects.filter(user_id=user_id).values()
    return perm[0]

def aprova_edital(request):
    try:
        status_aproval = Edital.objects.filter(~Q(status=3)).values()[0]
    except:
        status_aproval = []

    if status_aproval:
        btn_enviar = False
    else:
        btn_enviar = True
    metas = Edital.objects.raw("""
                                SELECT
                                DISTINCT 'normal' AS tipo_edital,
                                tpo.id,
                                tpo.diretoria,
                                tpo.turno,
                                tpo.trimestre,
                                tpo.vagas_totais,
                                tpo.carga_horaria,
                                tpo.carga_horaria_total,
                                tpo.previsao_inicio,
                                tpo.previsao_fim,
                                tpo.dias_semana,
                                tpo.previsao_abertura_edital,
                                tpo.previsao_fechamento_edital,
                                tpo.data_registro,
                                tpo.situacao,
                                tpo.jus_reprovacao,
                                tpo.curso_id,
                                tpo.eixo_id,
                                tpo.escola_id,
                                tpo.modalidade_id,
                                tpo.num_edital_id,
                                tpo.tipo_curso_id,
                                tpo.udepi_id,
                                tpo.curso_tecnico,
                                tpo.qualificacoes,
                                edt.num_edital,
                                edt.ano,
                                edt.dt_ini_edit,
                                edt.dt_fim_edit,
                                edt.dt_ini_insc,
                                edt.dt_fim_insc,
                                edt.status,
                                edt.pdf,
                                edt.motivo,
                                edt.escola_id,
                                edt.user_change_id,
                                tcur.tipo,
                                mdl.modalidade
                            FROM Turmas_planejado_orcado tpo
                            INNER JOIN edital_ensino edt ON tpo.num_edital_id = edt.id
                            INNER JOIN tipo_curso tcur ON tpo.tipo_curso_id = tcur.id
                            INNER JOIN modalidade mdl ON tpo.modalidade_id = mdl.id
                            WHERE dt_ini_edit IS NOT NULL AND STATUS=0
                            GROUP BY tpo.num_edital_id UNION ALL
                            SELECT
                                DISTINCT 'retificacao' AS tipo_edital,
                                tret.id,
                                tret.diretoria,
                                tret.turno,
                                tret.trimestre,
                                tret.vagas_totais,
                                tret.carga_horaria,
                                tret.carga_horaria_total,
                                tret.previsao_inicio,
                                tret.previsao_fim,
                                tret.dias_semana,
                                tret.previsao_abertura_edital,
                                tret.previsao_fechamento_edital,
                                tret.data_registro,
                                tret.situacao,
                                tret.jus_reprovacao,
                                tret.curso_id,
                                tret.eixo_id,
                                tret.escola_id,
                                tret.modalidade_id,
                                tret.num_edital_id,
                                tret.tipo_curso_id,
                                tret.udepi_id,
                                tret.curso_tecnico,
                                tret.qualificacoes,
                                edtr.num_edital,
                                edtr.ano,
                                edtr.dt_ini_edit,
                                edtr.dt_fim_edit,
                                edtr.dt_ini_insc,
                                edtr.dt_fim_insc,
                                edtr.status,
                                edtr.pdf,
                                edtr.motivo,
                                edtr.escola_id,
                                edtr.user_change_id,
                                tcur.tipo,
                                mdl.modalidade
                            FROM turmas_retificadas tret
                            INNER JOIN editais_retificados edtr ON tret.num_edital_id = edtr.id
                            INNER JOIN tipo_curso tcur ON tret.tipo_curso_id = tcur.id
                            INNER JOIN modalidade mdl ON tret.modalidade_id = mdl.id
                            WHERE dt_ini_edit IS NOT NULL AND STATUS=0
                            GROUP BY tret.num_edital_id
                               """)
    metas_gerais = Edital.objects.raw("""
                                SELECT
                                DISTINCT 'normal' AS tipo_edital,
                                tpo.id,
                                tpo.diretoria,
                                tpo.turno,
                                tpo.trimestre,
                                tpo.vagas_totais,
                                tpo.carga_horaria,
                                tpo.carga_horaria_total,
                                tpo.previsao_inicio,
                                tpo.previsao_fim,
                                tpo.dias_semana,
                                tpo.previsao_abertura_edital,
                                tpo.previsao_fechamento_edital,
                                tpo.data_registro,
                                tpo.situacao,
                                tpo.jus_reprovacao,
                                tpo.curso_id,
                                tpo.eixo_id,
                                tpo.escola_id,
                                tpo.modalidade_id,
                                tpo.num_edital_id,
                                tpo.tipo_curso_id,
                                tpo.udepi_id,
                                tpo.curso_tecnico,
                                tpo.qualificacoes,
                                edt.num_edital,
                                edt.ano,
                                edt.dt_ini_edit,
                                edt.dt_fim_edit,
                                edt.dt_ini_insc,
                                edt.dt_fim_insc,
                                edt.status,
                                edt.pdf,
                                edt.motivo,
                                edt.escola_id,
                                edt.user_change_id,
                                tcur.tipo,
                                mdl.modalidade
                            FROM Turmas_planejado_orcado tpo
                            INNER JOIN edital_ensino edt ON tpo.num_edital_id = edt.id
                            INNER JOIN tipo_curso tcur ON tpo.tipo_curso_id = tcur.id
                            INNER JOIN modalidade mdl ON tpo.modalidade_id = mdl.id
                            WHERE dt_ini_edit IS NOT NULL
                            GROUP BY tpo.num_edital_id UNION ALL
                            SELECT
                                DISTINCT 'retificacao' AS tipo_edital,
                                tret.id,
                                tret.diretoria,
                                tret.turno,
                                tret.trimestre,
                                tret.vagas_totais,
                                tret.carga_horaria,
                                tret.carga_horaria_total,
                                tret.previsao_inicio,
                                tret.previsao_fim,
                                tret.dias_semana,
                                tret.previsao_abertura_edital,
                                tret.previsao_fechamento_edital,
                                tret.data_registro,
                                tret.situacao,
                                tret.jus_reprovacao,
                                tret.curso_id,
                                tret.eixo_id,
                                tret.escola_id,
                                tret.modalidade_id,
                                tret.num_edital_id,
                                tret.tipo_curso_id,
                                tret.udepi_id,
                                tret.curso_tecnico,
                                tret.qualificacoes,
                                edtr.num_edital,
                                edtr.ano,
                                edtr.dt_ini_edit,
                                edtr.dt_fim_edit,
                                edtr.dt_ini_insc,
                                edtr.dt_fim_insc,
                                edtr.status,
                                edtr.pdf,
                                edtr.motivo,
                                edtr.escola_id,
                                edtr.user_change_id,
                                tcur.tipo,
                                mdl.modalidade
                            FROM turmas_retificadas tret
                            INNER JOIN editais_retificados edtr ON tret.num_edital_id = edtr.id
                            INNER JOIN tipo_curso tcur ON tret.tipo_curso_id = tcur.id
                            INNER JOIN modalidade mdl ON tret.modalidade_id = mdl.id
                            WHERE dt_ini_edit IS NOT NULL
                            GROUP BY tret.num_edital_id
                               """)
    # metas_gerais = Edital.objects.raw('Select DISTINCT * from Turmas_planejado_orcado INNER JOIN edital_ensino ON Turmas_planejado_orcado.num_edital_id = edital_ensino.id INNER JOIN tipo_curso ON Turmas_planejado_orcado.tipo_curso_id = tipo_curso.id INNER JOIN modalidade ON Turmas_planejado_orcado.modalidade_id = modalidade.id where dt_ini_edit is not NULL  group by Turmas_planejado_orcado.num_edital_id')
   


    return render(request, 'aprova_edital.html',{'permissoes': get_permission(request),'metas':metas,'metas_gerais':metas_gerais,'btn_enviar':btn_enviar})

def ajax_load_edital_v2(request):
    edital_id = request.GET['id']
    tipo_edital = request.GET['tipoEdital']
    if tipo_edital == 'normal':
        lancamentos = Edital.objects.filter(id=edital_id).select_related('escola').all()
    else:
        lancamentos = Editais_Retificados.objects.filter(id=edital_id).select_related('escola').all()

        
    edital = lancamentos[0]
    
    path_edital = request.get_full_path()
 
    return render(request, 'ajax_load_edital_v2.html', {'edital': edital,'tipo_edital':tipo_edital})

def aprovar_edital_gerado(request):
    idEdital = request.POST['edital']
    num_edital = int(request.POST['n_edital'])
    tipo_edital = request.POST['tipo_edital']
    aprovacao = int(request.POST['ap'])
    edital = Edital.objects.filter(num_edital = num_edital).values() if tipo_edital == 'normal' else Editais_Retificados.objects.filter(num_edital = num_edital).values()
    print('----------------------------')
    print(edital[0])

    if aprovacao == 3:
        idtbledital = edital[0]['id']
        atualiza_status = Edital.objects.get(id = idEdital)  if tipo_edital == 'normal' else Editais_Retificados.objects.get(id = idEdital)
        atualiza_status.status = 3
        atualiza_status.user_change_id = request.user.id
        atualiza_status.save()

        todosEditais = Edital.objects.filter(~Q(status=3)| Q(status=4)).values() if tipo_edital == 'normal' else Editais_Retificados.objects.filter(~Q(status=3)| Q(status=4)).values()

        # todosEditais = todosEditais[0]
        if len(todosEditais) > 0:
            messages.success(request, 'Edital foi aprovado com sucesso!')
            return redirect('/aprovar-edital')
        else:
            completeTask = getInstance(processName,'ConferiraprovarOEditalChecklistSGEVariavelEditalTemAlteracoesTask',request)
            messages.success(request, 'Edital foi aprovado com sucesso! Processo em andamento...')
            return redirect('/aprovar-edital')
        
    elif aprovacao == 1:
        motivo = request.POST['motivo']
        cria_status = Edital.objects.get(id = idEdital) if tipo_edital == 'normal' else Editais_Retificados.objects.get(id = idEdital)
        cria_status.status = 1
        cria_status.motivo = motivo
        cria_status.dt_ini_edit = None
        cria_status.dt_fim_edit = None
        cria_status.dt_ini_insc = None
        cria_status.dt_fim_insc = None
        cria_status.user_change_id = request.user.id
        cria_status.save()
        messages.success(request, 'Edital foi reprovado com sucesso!')
        return redirect('/aprovar-edital')
