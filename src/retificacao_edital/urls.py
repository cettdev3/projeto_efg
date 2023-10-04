from django.urls import path
from .views import retificar_edital,load_turmas_edital,load_turmas_edital_retificacao

urlpatterns = [
    path('retificar-edital', retificar_edital),
    path('ajax/ajax-load-turmas-edital', load_turmas_edital),
    path('ajax/load-turmas-por-edital', load_turmas_edital_retificacao),
]
