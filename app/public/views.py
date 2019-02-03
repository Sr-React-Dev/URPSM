from __future__ import absolute_import
from datetime import datetime
from django.views.generic import TemplateView, ListView, DetailView, FormView
from django.http.response import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required
from django.core.urlresolvers import reverse_lazy, reverse
# from django.core import serializers
from django.utils.safestring import mark_safe
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.db.models import Count, Max
from django.shortcuts import redirect, get_object_or_404, get_list_or_404
from django.utils.translation import ugettext_lazy as _
from .forms import ContactForm
from app.client.models import Client
from app.phone.models import Model
from app.component.models import Component
from app.phone.models import Brand
from app.shop.models import Shop
from app.server.models import Server
from app.ticket.models import OrderTicket
from app.order.models import ServerOrder, COMPLETED, CANCELLED, REJECTED
from app.ureview.models import ShopReview, ServerReview
from app.order.models import ShopOrder
from app.phone.models import Model
from braces.views import LoginRequiredMixin
from .geo import get_place
import json
from el_pagination.views import AjaxListView
from simplecities.models import City, Country
from mobilify.settings import DEFAULT_FROM_EMAIL
from .models import Contact
# from haystack.utils.geo import Point




class Home(TemplateView):
    template_name = 'urpsm/v2/public/index_v3.html'

    def get(self, request, *args, **kwargs):
        # if request.user.is_authenticated():
        #     return redirect(reverse_lazy('shop-position'))
        context = self.get_context_data(**kwargs)
        # context['form'] = ContactForm()
        context['registred_shops'] = self.registred_shops()
        context['repaired_phones'] = self.repaired_phones()
        context['best_reviewed_shops'] = self.best_reviewed_shops()
        context['popular_repaired_phones'] = self.popular_repaired_phones()
        context['popular_server'] = self.popular_server()
        context['registred_servers'] = self.registred_servers()
        context['unlocked_phones'] = self.unlocked_phones()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = ContactForm(request.POST)
        if form.is_valid():
            name  = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = 'Name: ' + name + '\n' + form.cleaned_data['message']
            send_mail('From Unlock Repair Phone Shop Manager', message, email, [
                      settings.DEFAULT_FROM_EMAIL, ], fail_silently=False)

        context['form'] = form
        return self.render_to_response(context)

    def registred_shops(self):
        return Shop.objects.filter(blocked=False).count() or 0
    def unlocked_phones(self):
        return ServerOrder.objects.filter(status='COMPLETED').count() or 0
    def repaired_phones(self):
        return Client.objects.select_related('brand').filter(
             deleted=False, paid=True, status='r').count() or 0
    def best_reviewed_shops(self):
        return Shop.objects.filter(blocked=False).exclude(average_rating=None).order_by('-average_rating')[:8]
    def popular_repaired_phones(self):
        return Model.objects.extra(
            select={'fieldsum': 'repaired_items + repairing_request + unlocking_request + unlocked_items'},
            order_by=('-fieldsum',))[:8]

    def popular_server(self):
        return Server.objects.filter(blocked=False).order_by('-average_rating')[:6]
    # def satisfied_users(self):
        # return ShopReview.objects.filter(rating__gte=4).distinct().count() or 0
    def registred_servers(self):
        return Server.objects.filter(blocked=False).count() or 0



class ShopPositionView(ListView):
    model = Shop
    template_name = "urpsm/v2/public/shop_map_markup.html"

    # def get_queryset(self, latLng):
    #     return Shop.geo_shops.get_shops_by_coords(latLng)

    def get(self, request, *args, **kwargs):
        if 'latLng' in request.GET:
            latLng  = request.GET.get('latLng') 
            place   = get_place(latLng, 16093)
            city    = place[0]
            country = place[2]
            self.object_list = self.get_queryset()
            shop_list = self.object_list.filter(city__name__icontains=city[:5], country__name=country).values('address', 'name', 'location','logo','city__name', 'country__name')
            return JsonResponse(list(shop_list), safe=False)
        else:
            self.object_list = None
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)

class SearchShopsByCountryAndCity(AjaxListView):
    model               = Shop
    template_name       = "urpsm/v2/public/search_shops_v2.html"
    page_template       = "urpsm/v2/public/search_shops_result_box_v2.html"
    context_object_name = 'shops'

    def get_context_data(self, **kwargs):
        context = super(SearchShopsByCountryAndCity, self).get_context_data(**kwargs)
        context['result_count'] = self.get_queryset().count()
        # print self.request.GET
        try:
            if 'q' in request.GET:
                city,country = map(capitalize, q.split('-'))
        except:
            try:
                city    = get_object_or_404(City, pk=int(self.kwargs['city'])).name
                country = get_object_or_404(Country, pk=int(self.kwargs['country'])).name
            except:
                pass
        try:
            context['city']    =  city
            context['country'] = country
        except:
            pass
        return context

    def get_queryset(self):
        qs = super(SearchShopsByCountryAndCity, self).get_queryset()
        try:
            return qs.filter(city__pk=int(self.kwargs['city']), country__pk=int(self.kwargs['country']))
        except:
            return qs


class ShopDetailView(DetailView, AjaxListView):
    template_name = 'urpsm/v2/public/shop_detail_v2.html'
    model = Shop
    context_object_name = 'shop'
    page_template  = "urpsm/v2/public/shop_review_box_v2.html"
    object_list    = []

    def get_context_data(self, **kwargs):
        context = super(ShopDetailView, self).get_context_data(**kwargs)
        context['reviews'] = ShopReview.objects.filter(shop=self.get_object()).values('pk', 'content', 'rating', 'user__username','language','creation_date').order_by('-creation_date')
        context['page_template'] =  "urpsm/v2/public/shop_review_box_v2.html"
        return context

    def get_object(self, query_set=None):
        return get_object_or_404(Shop, pk=int(self.kwargs.get('shop', None)))

class LandingPageView(TemplateView):
    template_name = 'urpsm/v2/public/landing_page_v2.html'

class LevelPageView(TemplateView):
    template_name = 'urpsm/v2/public/levels_v2.html'

class RegistredShopView(AjaxListView):
    model          = Shop
    template_name  = "urpsm/v2/public/registred_shops_v2.html"
    page_template  = "urpsm/v2/public/registred_shop_box_v2.html"
    context_object_name = 'shops'

class PopularShopView(AjaxListView):
    model = Shop
    template_name = "urpsm/v2/public/search_shops_v2.html"
    page_template  = "urpsm/v2/public/search_shops_result_box_v2.html"
    context_object_name = 'shops'
    def get_queryset(self):
        qs = super(PopularShopView, self).get_queryset()
        return qs.exclude(average_rating=None).order_by('-average_rating')

class RegistredServerView(AjaxListView):
    model = Server
    template_name = "urpsm/v2/public/registred_servers_v2.html"
    page_template  = "urpsm/v2/public/registred_server_box_v2.html"
    context_object_name = 'servers'

class UnlockedPhoneView(AjaxListView):
    model = Model
    template_name = "urpsm/v2/public/unlocked_phones_v2.html"
    page_template  = "urpsm/v2/public/unlocked_phone_box_v2.html"
    context_object_name = 'phones'

class RepairedPhoneView(AjaxListView):
    model = Model
    template_name = "urpsm/v2/public/repaired_phones_v2.html"
    page_template  = "urpsm/v2/public/repaired_phone_box_v2.html"
    context_object_name = 'phones'

class PopularPhoneView(AjaxListView):
    model = Model
    template_name = "urpsm/v2/public/repaired_phones_v2.html"
    page_template  = "urpsm/v2/public/repaired_phone_box_v2.html"
    context_object_name = 'phones'

    def get_queryset(self):
        qs = super(PopularPhoneView, self).get_queryset()
        # try:
        return Model.objects.extra(
            select={'fieldsum': 'repaired_items + repairing_request + unlocking_request + unlocked_items'},
            order_by=('-fieldsum',))
        # except:
            # return qs



class ModelDetailPage(DetailView):
    template_name = 'urpsm/v2/public/model_detail_v2.html'
    model = Model
    context_object_name = 'model'

    def get_object(self, query_set=None):
        try:
            return get_object_or_404(Model, slug=self.kwargs.get('model', None), brand__slug=self.kwargs.get('brand', None))
        except:
            return Model.objects.filter(slug=self.kwargs.get('model', None), brand__slug=self.kwargs.get('brand', None))[0]

   

class BrandModelListPage(ListView):
    template_name = 'urpsm/public/brand_model_v2.html'
    model         = Model

class AboutUsView(TemplateView):
    template_name = 'urpsm/v2/public/aboutus_v2.html'
        
class TermsView(TemplateView):
    template_name = 'urpsm/v2/public/terms.html'

class PrivacyView(TemplateView):
    template_name = 'urpsm/v2/public/privacy.html'

class ThankyouView(TemplateView):
    template_name = 'urpsm/v2/public/thankyou_v2.html'

class ContactView(FormView):
    form_class = ContactForm
    template_name = 'urpsm/v2/public/contact_v2.html'
    success_url   = reverse_lazy('thankyou')

    def form_valid(self, form):
        if form.is_valid():
            feedback =unicode(_('We had received your message. Thank you'))
            subject = "[URPSM]: %s"  % form.cleaned_data['subject']
            email   = form.cleaned_data['email']
            send_mail(subject, feedback, settings.DEFAULT_FROM_EMAIL, [ email, ], fail_silently=False)
            contact = form.instance.save()

        return  redirect(self.success_url)

class Error404View(TemplateView):
    template_name = "urpsm/v2/error404_v2.html"

@staff_member_required
def send_feedback(request):
    try:
        contact  = request.POST['contact']
        subject  = request.POST['subject']
        feedback = request.POST['feedback']
        email    = request.POST['email']
        try:
            subject = "[URPSM]: %s"  % subject
            send_mail(subject, feedback, settings.DEFAULT_FROM_EMAIL, [email, ], fail_silently=False)
        except Exception as e:
            print e


        contact = Contact.objects.get(pk=int(contact))
        contact.feedback = feedback
        contact.processed = True
        contact.save()
        return JsonResponse({'status':True})
    except Exception as e:
        print e
        return JsonResponse({'status':False})


from .forms import BrandSearchForm

class BrandDetailView(DetailView, AjaxListView):
    template_name       = 'urpsm/v2/public/brand_models_v2.html'
    model               = Brand
    context_object_name = 'brand'
    page_template       = "urpsm/v2/public/brand_model_box_v2.html"
    object_list         = []
    form_class          = BrandSearchForm

    def get_context_data(self, **kwargs):
        context           = super(BrandDetailView, self).get_context_data(**kwargs)
        context['models'] = self.get_object().brand_models.all().order_by('name')
        context['count']  = context['models'].count()
        context['form']   = self.form_class()
        context['page_template'] =  self.page_template
        return context

    def get_object(self, query_set=None):
        return get_object_or_404(Brand, slug=self.kwargs.get('brand', None))


    def post(self, *args, **kwargs):
        try:
            brand = self.request.POST.get('brand', None)
            model = self.request.POST.get('model', None)
            pk=int(brand)
            brand = Brand.objects.get(pk=pk).slug
            if model:
                model = Model.objects.get(pk=int(model)).slug
                return redirect('model', brand=brand, model=model)
            else:
                return redirect('brand', brand=brand)
        except:
            return redirect(self.request.META.get('HTTP_REFERER'))



