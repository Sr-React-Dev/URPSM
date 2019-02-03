# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.utils.encoding import force_text
from django.views.generic import FormView, TemplateView, ListView, View
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.contrib.auth import login, REDIRECT_FIELD_NAME
from django.contrib.auth.models import User, Group
from django.http import JsonResponse

from braces.views import LoginRequiredMixin, GroupRequiredMixin

from app.shop.models import ActionHistory
from .forms import ProfileForm, SignupForm, LoginForm, NewUserForm
from .models import Profile
import json
from app.shop.forms import ShopCreationForm, RegisterShopForm
from app.server.forms import RegisterServerForm
from app.account.forms import BusinessCreationForm, BusinessTypeForm



class HasBusinessMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.profile.phone:
            return redirect(reverse_lazy('profile'))
        elif not request.user.profile.shop and not request.user.profile.server:
            return redirect(reverse_lazy('create-business'))

        return super(HasBusinessMixin, self).dispatch(request, *args, **kwargs)


class CreateBusinessView(LoginRequiredMixin, FormView):
    template_name = 'urpsm/v2/accounts/business_v2.html'
    form_class = BusinessTypeForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect(reverse_lazy('login'))
        return super(CreateBusinessView, self).dispatch(request, *args, **kwargs)

    def form_invalid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = CreateBusinessView(self.request.POST)
        print context['form'].errors
        return self.render_to_response(context)

    def form_valid(self, form):
        print form.cleaned_data
        type = form.cleaned_data['business_type']
        if "shop" == type:
            return redirect(reverse_lazy('create-shop'))
        if "server" == type:
            return redirect(reverse_lazy('create-server'))
        return redirect(reverse_lazy('home'))


class RedirectUserToBusinessView(LoginRequiredMixin,View):
    def get(self, *args, **kwargs):
        if self.request.user.profile.shop:
            return HttpResponseRedirect(reverse_lazy('shop-position'))
        elif self.request.user.profile.server:
            return HttpResponseRedirect(reverse_lazy('server-position'))
        elif not self.request.user.profile.phone:
            return redirect(reverse_lazy('profile'))
        else:
            return redirect(reverse_lazy('create-business'))


class ProfileView(LoginRequiredMixin, FormView):
    template_name = 'urpsm/accounts/profile.html'
    form_class = ProfileForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect(reverse_lazy('login'))
        return super(ProfileView, self).dispatch(request, *args, **kwargs)

    # def get_success_url(self):
    #     return reverse_lazy('profile')

    def get_form_class(self):
        # self.profile = Signup.objects.get(user=self.request.user)
        self.profile = get_object_or_404(Profile, user=self.request.user)
        return super(ProfileView, self).get_form_class()

    def get_initial(self):
        initial = super(ProfileView, self).get_initial()
        initial['first_name'] = self.profile.user.first_name
        initial['last_name'] = self.profile.user.last_name
        initial['email'] = self.profile.user.email
        initial['phone'] = self.profile.phone
        return initial

    def form_valid(self, form):
        self.profile.user.first_name = form.cleaned_data['first_name']
        self.profile.user.last_name = form.cleaned_data['last_name']
        if self.profile.user.email != form.cleaned_data['email']:
            self.profile.change_email(form.cleaned_data['email'])
        self.profile.phone = form.cleaned_data['phone']
        self.profile.save()
        self.profile.user.save()
        if self.request.user.profile.shop:
            return redirect(reverse_lazy('shop-position'))
        elif self.request.user.profile.server:
            return redirect(reverse_lazy('server-position'))
        else:
            return redirect(reverse_lazy('create-business'))


class ChangeEmailView(LoginRequiredMixin, TemplateView):
    template_name = 'urpsm/accounts/email_confirmation.html'

    def get(self, request, *args, **kwargs):
        email_confirmation_key = self.kwargs.get('confirmation_key', None)
        account = get_object_or_404(
            Profile, email_confirmation_key=email_confirmation_key)
        if account:
            account.user.email = account.unconfirmed_email
            account.user.save()
            messages.success(
                request, _(u'Your email address has been changed.'), fail_silently=True)
            return redirect(reverse_lazy('profile'))
        else:
            messages.error(request, _(u'Invalid confirmation key.'))
            return redirect('/')
        return super(ChangeEmailView, self).get(request, *args, **kwargs)

def errors_response(form1, form2, form3=False):
    form_errors = {}
    for field, errors in form1.errors.iteritems():
        form_errors[field] = {}
        index = 1
        for error in errors:
            form_errors[field].update({index:error})
            index = index+1
    for field, errors in form2.errors.iteritems():
        form_errors[field] = {}
        index = 1
        for error in errors:
            form_errors[field].update({index:error})
            index = index+1
    if form3:
        for field, errors in form3.errors.iteritems():
            form_errors[field] = {}
            index = 1
            for error in errors:
                form_errors[field].update({index:error})
                index = index+1
    return JsonResponse({'status':False,'error':form_errors})

def form_errors_response(forms):
    errors = {}
    for form in forms:
        errors.update(json.loads( form.errors.as_json() ) )
    return JsonResponse({"status":False, "error":errors})




class CreateUserView(TemplateView):
    template_name = 'urpsm/v2/accounts/register_form_v2.html'
    form_signup   = SignupForm
    business_form = BusinessCreationForm
    shop_form     = RegisterShopForm
    server_form   = RegisterServerForm
    # form_class = SignupForm

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(request, **kwargs)
        return self.render_to_response(context)

    def get_context_data(self, request=False, **kwargs):
        context = super(CreateUserView, self).get_context_data(**kwargs)
        context['form'] = self.form_signup()
        try:
            context['business_form'] = self.business_form(initial={'business_type':request.GET['business']})
            context['preselect_busisness'] = True
        except:
            context['business_form'] = self.business_form()
        return context

    def post(self, request, *args, **kwargs):
        # print request.POST
        context = self.get_context_data(**kwargs)
        form = self.form_signup(request.POST)
        business_form = self.business_form(request.POST)
        if form.is_valid() and business_form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            if business_form.cleaned_data['business_type'] == 'shop':
                request.POST._mutable = True
                request.POST['shop_phone'] = request.POST['phone']
                request.POST['shop_email'] = request.POST['email']
                shop_form = self.shop_form(request.POST)
                if shop_form.is_valid():
                    shop = shop_form.save(commit=True)
                    user.save()
                    user.profile.shop  = shop
                    user.profile.phone = request.POST['phone']
                    # user.profile.save()
                else:
                    return form_errors_response([form, business_form, shop_form])
                    # return errors_response(form, business_form, shop_form)
            elif business_form.cleaned_data['business_type'] == 'server':
                request.POST._mutable = True
                request.POST['server_phone'] = request.POST['phone']
                request.POST['server_email'] = request.POST['email']
                server_form = self.server_form(request.POST)
                if server_form.is_valid():
                    server = server_form.save(commit=True)
                    user.save()
                    user.profile.server = server
                    user.profile.phone  = request.POST['phone']
                    # user.profile.save()
                else:
                    # return errors_response(form, business_form, server_form)
                    return form_errors_response([form, business_form, server_form])

            user.profile.is_admin = True
            user.profile.save()
            try:
                user.profile.activation_email()
            except Exception as e:
                print e

            # Adding the user to the administrator group
            try:
                group = Group.objects.get(name='Administrator')
                group.user_set.add(user)
            except:
                pass

            return JsonResponse({'status':True})
        else:
            return form_errors_response([form, business_form])
            # return errors_response(form, business_form)

        return self.render_to_response(context)

        # def form_valid(self, form):
        #     email = form.cleaned_data['email']
        #     username = form.cleaned_data['username']
        #     password = form.cleaned_data['password1']
        #     shop_name = form.cleaned_data['shop_name']
        #     shop_phone = form.cleaned_data['shop_phone']
        #     first_name = form.cleaned_data['first_name']
        #     last_name = form.cleaned_data['last_name']
        # shop = Shop.objects.get_or_create(name=shop_name, shop_name=shop_phone)
        #     account = Signup.objects.create_user(username, email, password)
        # account.user_profile.shop = shop
        # account.user_profile.save()
        # account.first_name = first_name
        # account.last_name = last_name
        # account.save()
        #     return super(CreateUserView, self).form_valid(form)

        # def get(self, request, *args, **kwargs):
        #     if request.user.is_authenticated():
        #         return redirect('/')
        #     else:
        #         form_class = self.get_form_class()
        #         form = self.get_form(form_class)
        #         return self.render_to_response(self.get_context_data(form=form))

        # def get_success_url(self):
        #     return reverse_lazy('email_confirmation')


class EmailConfirmationView(TemplateView):
    template_name = 'urpsm/v2/accounts/registration_done.html'


class AccountActivationView(TemplateView):
    template_name = 'urpsm/v2/accounts/registration_complete.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('/')
        else:
            activation_key = self.kwargs.get('activation_key', None)
            account = get_object_or_404(
                Profile, activation_key=activation_key)
            print account.user.is_active
            if account:
                if account.user.is_active:
                    return redirect(reverse_lazy('login'))
                else:
                    Profile.objects.activate_user(activation_key)

        return super(AccountActivationView, self).get(request, *args, **kwargs)


class LoginView(FormView):
    template_name = 'urpsm/v2/accounts/login_form_v2.html'
    form_class = LoginForm
    success_url = reverse_lazy('profile')

    # def clean(self):
    #     username = self.cleaned_data['username']
    #     password = self.cleaned_data['password']
    #     errors = []
    #     user = authenticate(username=username,
    #                         password=password, errors=errors)
    #     raise self.ValidationError('Foobar error ')
    #     return self.cleaned_data

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        self.request.session.set_expiry(60 * 60)
        return super(LoginView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        print 'is_authenticated', request.user.is_authenticated()
        if request.user.is_authenticated():
            if request.user.profile.shop:
                return redirect(reverse_lazy('shop-position'))
            elif request.user.profile.server:
                return redirect(reverse_lazy('server-position'))
            elif not request.user.profile.phone:
                return redirect(reverse_lazy('profile'))
            else:
                return redirect(reverse_lazy('create-business'))

        else:
            form_class = self.get_form_class()
            form = self.get_form(form_class)
            return self.render_to_response(self.get_context_data(LANGUAGE_CODE=request.LANGUAGE_CODE, form=form))


class UserView(LoginRequiredMixin,GroupRequiredMixin, ListView):
    template_name = 'urpsm/accounts/index.html'
    model = Profile
    context_object_name = 'users'
    paginate_by = 16
    group_required = u'Administrator'

    def get_queryset(self):
        return Profile.objects.select_related().filter(shop=self.request.user.profile.shop, user__is_staff=False)


class AddUserView(LoginRequiredMixin,GroupRequiredMixin, TemplateView):
    template_name = 'urpsm/accounts/new_user.html'
    form = NewUserForm
    group_required = u'Administrator'

    def get_context_data(self, **kwargs):
        context = super(AddUserView, self).get_context_data(**kwargs)
        context['form'] = self.form()
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = self.form(request.POST)
        context['form'] = form
        if form.is_valid():
            phone = form.cleaned_data['phone']
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            user.profile.phone = phone
            user.profile.is_admin = False

            # Adding the user to the selected group
            group = Group.objects.get(pk=form.cleaned_data['groups'])
            if group.name == 'Administrator':
                user.profile.is_admin = True
            if group.name != 'Administrator' and group.name != 'Technician' and group.name != 'Worker':
                return HttpResponse("Invalid group")
            group.user_set.add(user)
            ActionHistory.objects.create(shop=request.user.profile.shop, action="New User added #" + user.username,
                                         user=self.request.user)

            user.profile.shop = request.user.profile.shop
            user.profile.save()
            user.profile.activation_email()

            return redirect(reverse_lazy('users'))
        return self.render_to_response(context)


class DeleteUserView(LoginRequiredMixin, GroupRequiredMixin, View):
    group_required = u'Administrator'

    def get(self, *args, **kwargs):
        user = get_object_or_404(
            User, pk=self.kwargs.get('pk', None), profile__shop=self.request.user.profile.shop)
        user.delete()
        ActionHistory.objects.create(shop=self.request.user.profile.shop, action="User deleted #" + user.pk,
                                     user=self.request.user)
        return redirect(reverse_lazy('users'))


class BlockUserView(LoginRequiredMixin, GroupRequiredMixin, View):
    group_required = u'Administrator'

    def get(self, *args, **kwargs):
        user = get_object_or_404(
            User, pk=self.kwargs.get('pk', None), profile__shop=self.request.user.profile.shop)
        user.block_access = True
        ActionHistory.objects.create(shop=self.request.user.profile.shop, action="User blocked #" + user.username,
                                     user=self.request.user)
        user.save()
        return redirect(reverse_lazy('users'))

class Error404View(TemplateView):
    template_name = "urpsm/v2/error404_v2.html"