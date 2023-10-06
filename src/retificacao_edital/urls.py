from django.urls import path
from .views import remover_turma_retificada,load_turmas_retificadas,retificar_edital,load_turmas_edital,load_turmas_edital_retificacao,load_edital_exist,retifica_turma_edital,redefinir_retificacao

urlpatterns = [
    path('retificar-edital', retificar_edital),
    path('ajax/ajax-load-turmas-edital', load_turmas_edital),
    path('ajax/ajax-load-turmas-retificadas', load_turmas_retificadas),
    path('ajax/load-turmas-por-edital', load_turmas_edital_retificacao),
    path('ajax/load-edital-exist', load_edital_exist),
    path('ajax/realiza-retificacao', retifica_turma_edital),
    path('ajax/redefinir-retificacao', redefinir_retificacao),
    path('ajax/remove-turmas-retificadas', remover_turma_retificada),
]
