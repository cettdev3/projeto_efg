from DivisaoDeMetas.forms import DivisaoDeMetasForm, DivisaoDeMetasFilterFormHelper, DivisaoDeMetasFormDelete
from DivisaoDeMetas.tables import DivisaoDeMetasTable
from DivisaoDeMetas.filters import DivisaoDeMetasFilter
from DivisaoDeMetas.models import DivisaoDeMetasPorEscola
from django_tables2.views import SingleTableMixin
from django_tables2.export.views import ExportMixin
from django_tables2.paginators import LazyPaginator
from django_filters.views import FilterView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import ModelFormMixin
from django.views.generic.base import ContextMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from appprojeto1.views import get_permission


class DivisaoDeMetasContextMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permissoes'] = get_permission(self.request)
        return context


class FilteredSingleTableView(SingleTableMixin, FilterView):
    formhelper_class = None

    def get_filterset(self, filterset_class):
        kwargs = self.get_filterset_kwargs(filterset_class)

        if 'clean' in self.request.GET:
            kwargs['data'] = None

        filterset = filterset_class(**kwargs)
        filterset.form.helper = self.formhelper_class()
        return filterset


class DivisaoDeMetasView(LoginRequiredMixin, ExportMixin, FilteredSingleTableView, DivisaoDeMetasContextMixin):
    login_url = '/'
    table_class = DivisaoDeMetasTable
    filterset_class = DivisaoDeMetasFilter
    formhelper_class = DivisaoDeMetasFilterFormHelper
    paginator_class = LazyPaginator
    exclude_columns = ('actions', )


class DivisaoDeMetasDetailView(LoginRequiredMixin, ModelFormMixin, DetailView, DivisaoDeMetasContextMixin):
    login_url = '/'
    form_class = DivisaoDeMetasForm
    model = DivisaoDeMetasPorEscola


class DivisaoDeMetasCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView, DivisaoDeMetasContextMixin):
    login_url = '/'
    form_class = DivisaoDeMetasForm
    model = DivisaoDeMetasPorEscola

    def form_valid(self, form):
        meta = form.save(commit=False)
        meta.carga_horaria = meta.carga_horaria_total
        query = DivisaoDeMetasPorEscola.objects.filter(
            escola_id=meta.escola,
            ano=meta.ano,
            semestre=meta.semestre,
            tipo_id=meta.tipo,
            modalidade_id=meta.modalidade,
        ).count()

        if query > 0:
            messages.error(self.request, 'Meta já cadastrada.')
            return super().form_invalid(form)
        meta.save()
        messages.success(self.request, 'Meta cadastrada com sucesso.')
        return super().form_valid(form)


class DivisaoDeMetasUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView, DivisaoDeMetasContextMixin):
    login_url = '/'
    form_class = DivisaoDeMetasForm
    model = DivisaoDeMetasPorEscola

    def form_valid(self, form):
        self.object.carga_horaria = (
            self.object.carga_horaria_total -
            form.cleaned_data['carga_horaria_total_atual']
        ) + self.object.carga_horaria

        if self.object.carga_horaria < 0:
            messages.error(
                self.request, 'O saldo não pode ser menor que zero.')
            return super().form_invalid(form)

        form.save()
        messages.success(self.request, 'Meta atualizada.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['carga_horaria_total_atual'] = self.object.carga_horaria_total
        context['form'] = DivisaoDeMetasForm(
            instance=self.object,
            initial={'carga_horaria_total_atual': self.object.carga_horaria_total}
        )
        return context


class DivisaoDeMetasDeleteView(LoginRequiredMixin, ModelFormMixin, DeleteView, DivisaoDeMetasContextMixin):
    login_url = '/'
    form_class = DivisaoDeMetasFormDelete
    model = DivisaoDeMetasPorEscola
