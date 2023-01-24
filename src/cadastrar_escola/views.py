from django.shortcuts import render, redirect
from appprojeto1.models import Metas_escolas,User_permission,User,Metas_efg
from django.contrib import messages

def getUserlogin(request):
    username = request.user
    id_user = User.objects.filter(username=username).values()
    return id_user[0]['id']

def get_permission(request):

    user_id = getUserlogin(request)
    perm = User_permission.objects.filter(user_id=user_id).values()
    return perm[0]
# Create your views here.

def cadastrar_escolas(request):
    escolas = Metas_escolas.objects.all()
    print(escolas)
    
    return render(request, 'cadastrar_escolas.html', {'escolas': escolas,'permissoes': get_permission(request)})

def cad_escola(request):
    escola = request.POST['escola']
    tipo = request.POST['tipo']
    email = request.POST['email']
    telefone = request.POST['telefone']

    cadEscola = Metas_escolas.objects.create(escola = escola,tipo = tipo, email = email,telefone = telefone)

    messages.success(request, 'Escola cadastrada com sucesso')
    return redirect('/cadastrar-escola')

def delete_escola(request):
    codigo = request.POST['id_deleta']
    escola = Metas_escolas.objects.get(id=codigo)
    print(escola)
    escola.delete()

    messages.success(request, 'Escola removida com sucesso!')
    return redirect('/cadastrar-escola')