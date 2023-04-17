from django.shortcuts import render, redirect
from appprojeto1.models import User, User_permission,Edital,Users_ids
from django.contrib import messages
from django.db.models import Q
from requests.auth import HTTPBasicAuth
import requests as req
import json
import envconfiguration as config

host = config.CAMUNDA_URL #type:ignore
# host = 'https://processos.cett.dev.br/engine-rest/'
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
    metas = Edital.objects.raw("Select DISTINCT * from Turmas_planejado_orcado INNER JOIN edital_ensino ON Turmas_planejado_orcado.num_edital_id = edital_ensino.id INNER JOIN tipo_curso ON Turmas_planejado_orcado.tipo_curso_id = tipo_curso.id INNER JOIN modalidade ON Turmas_planejado_orcado.modalidade_id = modalidade.id where dt_ini_edit is not NULL and status= 0  group by Turmas_planejado_orcado.num_edital_id")
    metas_gerais = Edital.objects.raw('Select DISTINCT * from Turmas_planejado_orcado INNER JOIN edital_ensino ON Turmas_planejado_orcado.num_edital_id = edital_ensino.id INNER JOIN tipo_curso ON Turmas_planejado_orcado.tipo_curso_id = tipo_curso.id INNER JOIN modalidade ON Turmas_planejado_orcado.modalidade_id = modalidade.id where dt_ini_edit is not NULL  group by Turmas_planejado_orcado.num_edital_id')
   


    return render(request, 'aprova_edital.html',{'permissoes': get_permission(request),'metas':metas,'metas_gerais':metas_gerais,'btn_enviar':btn_enviar})

def ajax_load_edital_v2(request):
    edital_id = request.GET['id']
    lancamentos = Edital.objects.filter(id=edital_id).select_related('escola').all()
    edital = lancamentos[0]
    path_edital = request.get_full_path()
    print(path_edital)
    
    return render(request, 'ajax_load_edital_v2.html', {'edital': edital})

def aprovar_edital_gerado(request):
    idEdital = request.POST['edital']
    num_edital = int(request.POST['n_edital'])
  
    aprovacao = int(request.POST['ap'])
    edital = Edital.objects.filter(num_edital = num_edital).values()
    print('----------------------------')
    print(edital[0])

    if aprovacao == 3:
        idtbledital = edital[0]['id']
        atualiza_status = Edital.objects.get(id = idtbledital)
        atualiza_status.status = 3
        atualiza_status.user_change = int(request.user.id)
        atualiza_status.save()

        todosEditais = Edital.objects.filter(~Q(status=3)| Q(status=4)).values()
        print(len(todosEditais))
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
        cria_status = Edital.objects.get(id = idtbledital)
        cria_status.status = 1
        cria_status.motivo = motivo
        cria_status.dt_ini_edit = None
        cria_status.dt_fim_edit = None
        cria_status.dt_ini_insc = None
        cria_status.dt_fim_insc = None
        cria_status.user_change = request.user.id
        cria_status.save()
        messages.success(request, 'Edital foi reprovado com sucesso!')
        return redirect('/aprovar-edital')
