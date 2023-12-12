from django.shortcuts import render, redirect
from appprojeto1.models import Metas_escolas, User_permission, User
from django.contrib import messages


def getUserlogin(request):
    username = request.user
    id_user = User.objects.filter(username=username).values()
    return id_user[0]["id"]


def get_permission(request):
    user_id = getUserlogin(request)
    print(user_id)
    perm = User_permission.objects.filter(user_id=user_id).values()
    return perm[0]


# Create your views here.


def cadastrar_escolas(request):
    escolas = Metas_escolas.objects.all()

    return render(
        request,
        "cadastrar_escolas.html",
        {"escolas": escolas, "permissoes": get_permission(request)},
    )


def cad_escola(request):
    escola = request.POST["escola"]
    tipo = request.POST["tipo"]
    email = request.POST["email"]
    telefone = request.POST["telefone"]

    cadEscola = Metas_escolas.objects.create(
        escola=escola, tipo=tipo, email=email, telefone=telefone
    )

    messages.success(request, "Escola cadastrada com sucesso")
    return redirect("/cadastrar-escola")


def delete_escola(request):
    codigo = request.POST["id_deleta"]
    escola = Metas_escolas.objects.get(id=codigo)
    escola.delete()

    messages.success(request, "Escola removida com sucesso!")
    return redirect("/cadastrar-escola")


def edit_escola(request):
    codigo = request.POST["id_edit"]
    escola = request.POST["escolaModal"]
    tipo = request.POST["tipoModal"]
    email = request.POST["emailModal"]
    telefone = request.POST["telefoneModal"]

    escolaEdit = Metas_escolas.objects.get(id=codigo)

    escolaEdit.escola = escola
    escolaEdit.tipo = tipo
    escolaEdit.email = email
    escolaEdit.telefone = telefone

    escolaEdit.save()

    messages.success(request, "Escola editada com sucesso!")
    return redirect("/cadastrar-escola")
