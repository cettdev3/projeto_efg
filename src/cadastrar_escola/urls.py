from cadastrar_escola import views
from cadastrar_escola.views import cadastrar_escolas,cad_escola,delete_escola
from django.urls import path

urlpatterns = [
    path('cadastrar-escola', cadastrar_escolas, name='cadastrar-escola'),
    path('cad-escola', cad_escola, name='cad_escola'),
    path('delete-escola', delete_escola, name='delete-escola'),
   
]
