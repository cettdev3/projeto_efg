from django.urls import path
from .views import retificar_edital,load_turmas_edital

urlpatterns = [
    path('retificar-edital', retificar_edital),
    path('ajax/ajax-load-turmas-edital', load_turmas_edital),
]
