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
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages


class FilteredSingleTableView(SingleTableMixin, FilterView):
    formhelper_class = None

    def get_filterset(self, filterset_class):
        kwargs = self.get_filterset_kwargs(filterset_class)

        if 'clean' in self.request.GET:
            filterset = filterset_class()
        else:
            filterset = filterset_class(**kwargs)

        filterset.form.helper = self.formhelper_class()
        return filterset


class DivisaoDeMetasView(LoginRequiredMixin, ExportMixin, FilteredSingleTableView):
    login_url = '/'
    table_class = DivisaoDeMetasTable
    filterset_class = DivisaoDeMetasFilter
    formhelper_class = DivisaoDeMetasFilterFormHelper
    paginator_class = LazyPaginator
    exclude_columns = ('actions', )
    # table_pagination = {
    #     "per_page": 25
    # }


class DivisaoDeMetasDetailView(LoginRequiredMixin, ModelFormMixin, DetailView):
    login_url = '/'
    form_class = DivisaoDeMetasForm
    model = DivisaoDeMetasPorEscola


class DivisaoDeMetasCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
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


class DivisaoDeMetasUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
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

    def get_initial(self):
        context = {
            'carga_horaria_total_atual': self.object.carga_horaria_total
        }
        return context


class DivisaoDeMetasDeleteView(LoginRequiredMixin, ModelFormMixin, DeleteView):
    login_url = '/'
    form_class = DivisaoDeMetasFormDelete
    model = DivisaoDeMetasPorEscola
