# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, CreateView, TemplateView, ListView, View
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect, get_object_or_404, render
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http.response import Http404

from app.notifications.models import Notification
from app.order.models import ServerOrder
from mobilify.decorators import ajax_required
from .utils import detect_language
from json import dumps
from django.http.response import HttpResponse

from .models import ShopReview, OrderReview, ServerReview
from .forms import ServerReviewForm, ShopReviewForm

from app.shop.models import Shop
from app.server.models import Server
from app.client.models import Client

class ThankyouView(TemplateView):
	pass
    # template_name = "urpsm/ureview/thankyou.html"
    
@login_required
def create_server_review(request, pk):
	if not request.user.profile.shop:
		raise Http404(_('Your are not allowed to access this ressource'))
	context = dict()
	server = get_object_or_404(Server, pk=int(pk))

	if request.method == 'POST':
		form = ServerReviewForm(request.POST)
		if form.is_valid():
			review = form.save(commit=False)
			review.user = request.user
			review.server = server
			review.save()
			server.save()
			return redirect(reverse_lazy('thank-you'))

		else:
			context.update({'form':form})
	else:
		context.update({'form':ServerReviewForm()})
	return render(request, 'urpsm/ureview/review_form.html', context)


@ajax_required
def create_shop_review(request):
	client_id = request.POST.get('client',None)
	rating    = request.POST.get('rating',None)
	content   = request.POST.get('content',None)
	shop_id   = request.POST.get('shop',None)
	if shop_id:
		shop = get_object_or_404(Shop, pk=int(shop_id))
		print shop
	else:
		return HttpResponse( dumps({'status': 'NO shop'}), content_type="application/json")

	if client_id:
		client = get_object_or_404(Client, pk=int(client_id))
		# print client
	else:
		return HttpResponse( dumps({'status': 'No client'}), content_type="application/json")

	if rating and content:
		rating = int(rating)
		language = detect_language(content)
		# print language
		if not ShopReview.objects.filter(shop=shop, client=client).exists():
			review = ShopReview.objects.create(shop=shop, client=client, language=language, rating=rating, content=content)
			shop.save()
			users = User.objects.filter(profile__shop=shop)
			for user in users:
				user.profile.notify_new_client_review(shop, client)
			return HttpResponse( dumps({'status': True}), content_type="application/json")
		else:
			return HttpResponse( dumps({'status': False, 'message': unicode( _('This service has already been reviewed')) }), content_type="application/json")
	else:
		return HttpResponse( dumps({'status': False, 'message': unicode( _('Your review is not complete')) }), content_type="application/json")


@login_required
@csrf_exempt
def create_server_order_review(request):
	usr = request.user
	order_id = request.POST['orderid']
	order = ServerOrder.objects.get(pk=order_id)
	rating = float(request.POST['orderrating'])
	content = ""+request.POST['content']
	language = "eng"
	if not OrderReview.objects.filter(order=order).exists():
		OrderReview.objects.create(order=order,server=order.server,rating=rating,content=content,user=usr,language=language)
		ser = ServerReview.objects.create(server=order.server,rating=rating,shop=request.user.profile.shop,content=content,user=usr,language=language)
		Notification.objects.create(server=order.server,server_review=ser,notification_type='C')
		return HttpResponse("Order successfully saved",status=200)
	else:
		return HttpResponse("Rating already exist for the order")