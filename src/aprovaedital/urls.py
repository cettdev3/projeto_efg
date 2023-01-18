from aprovaedital import views
from aprovaedital.views import aprova_edital, ajax_load_edital_v2, aprovar_edital_gerado
from django.urls import path

urlpatterns = [
    path('aprovar-edital', aprova_edital, name='aprovar-edital'),
    path('ajax/ajax-load-turmas-v2', ajax_load_edital_v2),
    path('aprova-edital', aprovar_edital_gerado),
]
