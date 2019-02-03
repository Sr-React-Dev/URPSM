from __future__ import absolute_import
from django.views.generic import CreateView, ListView, View, TemplateView, DetailView
from django.shortcuts import redirect
from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from braces.views import LoginRequiredMixin, GroupRequiredMixin

from app.shop.models import ActionHistory
from .forms import CreateComponentForm, UpdateComponentForm
from .models import Component
from app.account.views import HasBusinessMixin
from app.search.backends import get_search_backend
from el_pagination.views import AjaxListView


class ComponentView(LoginRequiredMixin,GroupRequiredMixin, ListView):
    template_name = 'urpsm/components/index.html'
    context_object_name = 'components'
    model = Component
    paginate_by = 15
    group_required = [u'Administrator', u'Technician']

    def get_queryset(self):
        return Component.objects.select_related().filter(shop=self.request.user.profile.shop, deleted=False)


class CreateComponentView(LoginRequiredMixin,GroupRequiredMixin, CreateView):
    template_name = 'urpsm/components/create.html'
    form_class = CreateComponentForm
    group_required = [u'Administrator', u'Technician']

    def form_valid(self, form):
        component = form.save(commit=False)
        component.shop = self.request.user.profile.shop
        component.save()
        ActionHistory.objects.create(shop=component.shop, action="New Component added #" + str(component.pk), user=self.request.user)
        # component.save_m2m()
        return super(CreateComponentView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('components')


class UpdateComponentView(LoginRequiredMixin,GroupRequiredMixin, UpdateView):
    template_name = 'urpsm/components/update.html'
    form_class = UpdateComponentForm
    model = Component
    group_required = [u'Administrator', u'Technician']

    def get_object(self, queryset=None):
        return get_object_or_404(Component,
                                 pk=self.kwargs.get(self.pk_url_kwarg, None),
                                 shop=self.request.user.profile.shop)

    def form_valid(self, form):
        component = form.save(commit=False)
        component.shop = self.request.user.profile.shop
        component.save()
        ActionHistory.objects.create(shop=component.shop, action="Component updated #" + str(component.pk),
                                     user=self.request.user)
        # component.save_m2m()
        return super(UpdateComponentView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('components')


class DeleteComponentView(LoginRequiredMixin,GroupRequiredMixin, View):
    group_required = u'Administrator'

    def get(self, *args, **kwargs):
        component = get_object_or_404(Component,
                                      pk=self.kwargs.get('pk', None),
                                      shop=self.request.user.profile.shop, deleted=False)
        component.deleted = True
        component.save()
        ActionHistory.objects.create(shop=component.shop, action="Component Deleted #" + str(component.pk),
                                     user=self.request.user)
        return redirect(reverse_lazy('components'))

class ComponentDetailView(LoginRequiredMixin,GroupRequiredMixin, DetailView):
    template_name = 'urpsm/v2/components/component_detail_v2.html'
    model = Component
    context_object_name = 'component'
    group_required = [u'Administrator', u'Technician']

    def get_object(self, queryset=None):
        return get_object_or_404(Component, pk=self.kwargs.get('pk'), slug=self.kwargs.get('slug'))
            

    def get_context_data(self, **kwargs):
        context = super(ComponentDetailView, self).get_context_data(**kwargs)
        return context


class ComponentListView(LoginRequiredMixin,  HasBusinessMixin,GroupRequiredMixin, ListView):
    template_name = 'urpsm/v2/components/components_list_v2.html'
    context_object_name = 'components'
    model = Component
    paginate_by = 12
    group_required = [u'Administrator', u'Technician']

    def get_queryset(self):
        return Component.objects.select_related().filter(deleted=False, sold=False).exclude(shop=self.request.user.profile.shop)




class ComponentSearchView(LoginRequiredMixin, HasBusinessMixin, TemplateView, AjaxListView):
    template_name       = 'urpsm/v2/search/component_search_result_v2.html'
    model               = Component
    context_object_name ='component'
    page_template       = "urpsm/v2/search/component_search_result_box_v2.html"
    object_list         = []
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        backend = get_search_backend('default')
        query   = request.GET.get('q', '')
        context['query'] = query
        Components = self.model.objects.filter(sold=False, deleted=False)
        results    = backend.search(query, model_or_queryset=Components, operator="or")
        context['components'] = results
        return self.render_to_response(context)


    def get_context_data(self, **kwargs):
        context = super(ComponentSearchView, self).get_context_data(**kwargs)
        context['page_template'] =  "urpsm/v2/search/component_search_result_box_v2.html"
        context['object_list']   = []
        return context