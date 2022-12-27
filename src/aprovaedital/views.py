from django.shortcuts import render, redirect
from appprojeto1.models import Users,User_permission,Edital
from django.contrib import messages
from requests.auth import HTTPBasicAuth
import requests as req
import json

host = 'https://processos.cett.dev.br/engine-rest/'
processName = "SolicitarOfertaDeVaga"
autentication = HTTPBasicAuth('dmartins', 'CETT@2022')

def camundaPutVariable(taskId,variable,variableValue,type):
    #https://processos.cett.dev.br/engine-rest/task/bd7fa2eb-8536-11ed-ad45-0242ac130024/variables/alteracao
    headers = {'Content-type': 'application/json'}
    bodyJson = {"value" : variableValue, "type": type}
    putVariable = req.put(f"{host}task/{taskId}/variables/{variable}",json=bodyJson, auth=autentication, headers=headers)
    return True if putVariable.status_code == 204 else  False

def getInstance(processName, taskDefinition):
    taskDefinitionKey = taskDefinition
    url = f"{host}task?processDefinitionKey={processName}"
    requisicao = req.get(url, json={}, auth=autentication)
    retorno = requisicao.text
    json_object = json.loads(retorno)
    for dados in json_object:
        if dados['taskDefinitionKey'] == taskDefinitionKey:
            idTask = dados['id']
            headers = {'Content-type': 'application/json'}
            putvariable = camundaPutVariable(idTask,'alteracao','não','String')
            if putvariable == True:
                completeTask = req.post(
                    f"{host}task/{idTask}/complete", auth=autentication, headers=headers)
                if completeTask.status_code == 204:
                    print('Taks is completed!')
                    return True
                else:
                    return False
            else:
                return False


def getUserlogin(request):
    username = request.user
    id_user = Users.objects.filter(username=username).values()
    return id_user[0]['id']

def get_permission(request):
    user_id = getUserlogin(request)
    perm = User_permission.objects.filter(user_id=user_id).values()
    return perm[0]

def aprova_edital(request):
    metas = Edital.objects.raw("Select DISTINCT * from Turmas_planejado_orcado INNER JOIN edital_ensino ON Turmas_planejado_orcado.num_edital_id = edital_ensino.id INNER JOIN tipo_curso ON Turmas_planejado_orcado.tipo_curso_id = tipo_curso.id INNER JOIN modalidade ON Turmas_planejado_orcado.modalidade_id = modalidade.id where dt_ini_edit is not NULL and status= 0  group by Turmas_planejado_orcado.num_edital_id")
    return render(request, 'aprova_edital.html',{'permissoes': get_permission(request),'metas':metas})

def ajax_load_edital_v2(request):
    edital_id = request.GET['id']
    lancamentos = Edital.objects.filter(id=edital_id).select_related('escola').all()
    edital = lancamentos[0]
    path_edital = request.get_full_path()
    print(path_edital)
    
    return render(request, 'ajax_load_edital_v2.html', {'edital': edital})

def aprovar_edital_gerado(request):
    print(request.POST)
    num_edital = int(request.POST['n_edital'])
  
    aprovacao = int(request.POST['ap'])
    edital = Edital.objects.filter(num_edital = num_edital).values()
    print(edital)
    
    if aprovacao == 3:
        for edit in edital:
            # print(edital)
            idtbledital = edit['id']
            atualiza_status = Edital.objects.get(id = idtbledital)
            atualiza_status.status = 3
            atualiza_status.save()

        todosEditais = Edital.objects.filter(status=0).filter(status=1).filter(status=2).values()
        print(todosEditais)
        # todosEditais = todosEditais[0]
        if todosEditais:
            messages.success(request, 'Edital foi aprovado com sucesso!')
            return redirect('/aprovar-edital')
        else:
            completeTask = getInstance(processName,'ElaborarEdital')
            messages.success(request, 'Edital foi aprovado com sucesso!')
            return redirect('/aprovar-edital')

    elif aprovacao == 1:
        motivo = request.POST['motivo']
        atualiza_status = Edital.objects.get(id = idtbledital)
        atualiza_status.status = 1
        atualiza_status.motivo = motivo
        atualiza_status.dt_ini_edit = None
        atualiza_status.dt_fim_edit = None
        atualiza_status.dt_ini_insc = None
        atualiza_status.dt_fim_insc = None
        atualiza_status.save()
        messages.success(request, 'Edital foi reprovado com sucesso!')
        return redirect('/aprovar-edital')
