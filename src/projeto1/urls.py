"""projeto1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from appprojeto1 import views
from appprojeto1.views import Logout_Users, load_ch,buscar_saldo_replanejado, verifica_turmas_edital, load_municipios, cadastrar_udepi, Autenticar, apaga_orcamento, apagar_curso_escola, cad_curso_escola, cad_novo_curso, cadastrar_curso, cadastro_curso_escola, del_curso, editar_curso, editar_curso_escola, editar_orcamento, load_cht, load_cursos, load_eixos, load_funcoes_gerencia_cursos, load_funcoes_gerencia_eixo, load_funcoes_rp, load_funcoes_tabela, load_funcoes_total_horas, load_funcoes_vagas, apagar_meta, apagar_meta_sintetica, cad_metas, cad_metas_sintetica, cad_orcamento, cadastrar_meta_sintetica, load_funcoes_filter, cadastrar_metas, editar_meta, editar_metas_sintetica, editarmetas, load_funcoes_rubrica, load_modalidade, orcamento_plano_trabalho, realizar_solicitacao, view_eixos, view_geral, view_index, load_funcoes, ajax_load_turmas_edital, ajax_load_turmas_edital_filtro, atualiza_edital, gerenciar_usuarios, salvar_permissoes, enviar_planejamento, load_funcoes_permissoes, cadastrar_usuario,buscar_siga_selecao,replanejar_curso

urlpatterns = [
    path('admin/', admin.site.urls),
    path('eixos/', view_eixos),
    path('dologin', Autenticar, name='dologin'),
    path('logout', Logout_Users, name='Logout'),
    path('', view_geral),
    path('dashboard', view_index, name='Home'),
    path('ajax/load-funcoes', load_funcoes, name='ajax_load_funcoes'),
    path('ajax/ajax_load_vagas', load_funcoes_vagas, name='ajax_load_vagas'),
    path('ajax/ajax_load_eixos', load_eixos, name='ajax_load_eixos'),
    path('ajax/ajax_load_municipios', load_municipios,
         name='ajax_load_municipios'),
    path('ajax/ajax_load_tbleixos', load_funcoes_gerencia_eixo,
         name='ajax_load_funcoes_gerencia_eixo'),
    path('ajax/ajax_load_tblcursos', load_funcoes_gerencia_cursos,
         name='ajax_load_funcoes_gerencia_cursos'),
    path('ajax/ajax_load_modalidade', load_modalidade,
         name='ajax_load_modalidade'),
    path('ajax/ajax_load_recurso_planejado',
         load_funcoes_rp, name='ajax_load_horas'),
    path('ajax/ajax_load_total_horas', load_funcoes_total_horas,
         name='ajax_load_total_horas'),
    path('ajax/load-funcoes-filter', load_funcoes_filter,
         name='ajax_load_funcoes_filter'),
    path('ajax/ajax_load_tabela', load_funcoes_tabela,
         name='ajax_load_funcoes_tabela'),
    path('ajax/ajax_load_cursos', load_cursos, name='ajax_load_funcoes_cursos'),
    path('ajax/ajax_load_cht', load_cht, name='ajax_load_funcoes_cht'),
    path('ajax/ajax_load_carga_hr_curso', load_ch,
         name='ajax_load_carga_hr_curso'),
    path('ajax/get_cursos/', views.get_cursos, name='get_cursos'),
    path('ajax/get_eixos/', views.get_eixos, name='get_eixos'),
    path('realizar-solicitacao', realizar_solicitacao),
    path('cadastrar-metas', cadastrar_metas, name='cadastrar_metas'),
    path('cadmetas', cad_metas),
    path('apagar-meta', apagar_meta),
    path('editar-meta/<codigo>', editar_meta),
    path('editarmetas', editarmetas),
    path('cadastrar-metas-sinteticas', cadastrar_meta_sintetica,
         name='cadastrar-metas-sinteticas'),
    path('cadmetas-sintetica', cad_metas_sintetica),
    path('apagar-meta-sintetica', apagar_meta_sintetica),
    path('editar-metas-sintetica', editar_metas_sintetica),
    path('orcamento-plano-trabalho', orcamento_plano_trabalho,
         name='orcamento-plano-trabalho'),
    path('ajax/load-funcoes-orcamento', load_funcoes_rubrica,
         name='ajax_load_funcoes_orcamento'),
    path('cad-orcamento-plano-trabalho', cad_orcamento),
    path('edit-orcamento-plano-trabalho', editar_orcamento),
    path('apagar-orcamento', apaga_orcamento),
    path('cadastrar-curso-escola', cadastro_curso_escola),
    path('cad-curso-escola', cad_curso_escola),
    path('apagar-curso-escola', apagar_curso_escola),
    path('editar-curso-escola', editar_curso_escola),
    path('cadastrar-curso', cadastrar_curso, name='cadastrar-curso'),
    path('cad-new-curso', cad_novo_curso),
    path('del-curso', del_curso),
    path('editar-curso', editar_curso),
    path('cadastrar-udepi', cadastrar_udepi),
    path('solicitacaodeturmas/', include('SolicitacaoDeTurmas.urls')),
    path('divisaodemetas/', include('DivisaoDeMetas.urls')),
    path('aprova-cursos/', views.AprovarCursosView.as_view(),
         name='AprovarCursosView'),
    path('dash_aprovar/', views.DashboardAprovarCursosView.as_view(),
         name='DashboardAprovarCursosView'),
    path('aprova-cursos/<int:pk>/edit/',
         views.AprovarCursosUpdateView.as_view(), name='AprovarCursosUpdateView'),
    path('reprova-cursos/', views.ReprovaCursosUpdateView.as_view(),
         name='ReprovaCursosUpdateView'),
    path('verifica-turmas-edital', verifica_turmas_edital,
         name='verifica-turmas-edital'),
    path('ajax/ajax_load_turmas_edital', ajax_load_turmas_edital),
    path('ajax/ajax_load_turmas_edital_filtro', ajax_load_turmas_edital_filtro),
    path('ajax/ajax_load_perm', load_funcoes_permissoes),
    path('atualiza-edital', atualiza_edital),
    path('permissoes-usuarios', gerenciar_usuarios),
    path('salvar-permissoes', salvar_permissoes),
    path('enviar-planejamento', enviar_planejamento),
    path('cadastrar-usuario', cadastrar_usuario),
    path('buscar-siga-selecao', buscar_siga_selecao),

    path('', include('aprovaedital.urls')),
    path('', include('cadastrar_escola.urls')),
     path('', include('retificacao_edital.urls')),

    #replanejamento
    path('ajax/ajax-replanejar-curso', replanejar_curso),
    path('ajax/buscar-saldo-replanejado', buscar_saldo_replanejado),

]

