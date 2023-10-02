from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from appprojeto1.models import Edital
from appprojeto1.models import User, User_permission,Edital,Users_ids
from appprojeto1.models import Metas_efg
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

    editais =  metas = Edital.objects.raw("Select DISTINCT * from Turmas_planejado_orcado INNER JOIN edital_ensino ON Turmas_planejado_orcado.num_edital_id = edital_ensino.id INNER JOIN tipo_curso ON Turmas_planejado_orcado.tipo_curso_id = tipo_curso.id INNER JOIN modalidade ON Turmas_planejado_orcado.modalidade_id = modalidade.id where dt_ini_edit is not NULL and status= 0  group by Turmas_planejado_orcado.num_edital_id")


    return render(request, 'retificacao_edital.html', {'permissoes':get_permission(request),'editais':editais})

@login_required(login_url='/')
def load_turmas_edital(request):

    editalId = request.GET['editalId']
    turmas = Metas_efg.objects.filter(num_edital_id = editalId).all()
    return render(request, 'ajax/ajax_tbl_retificacao.html', {'editais':turmas})