from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from .models import Curso

from .forms import SolicitacaoDeTurmas
from appprojeto1.models import Users,User_permission
from appprojeto1.views import get_permission


def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SolicitacaoDeTurmas(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    elif request.method == 'GET':
        form = SolicitacaoDeTurmas()

    return render(request, 'form.html', {
            'form': form,
            'permissoes': get_permission(request)
        })

def processa_form(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SolicitacaoDeTurmas(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            form.save()
    elif request.method == 'GET':
        return HttpResponseRedirect('/form/')
    return HttpResponse(form)

def load_cursos(request):
    eixo_id = request.GET.get('eixo')
    cursos = Curso.objects.filter(eixos_id=eixo_id).order_by('curso')
    return render(request, 'ajax/cursos_dropdown_list_options.html', {'cursos': cursos})