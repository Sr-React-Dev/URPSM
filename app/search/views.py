from __future__ import unicode_literals

from django.core.paginator import Paginator, InvalidPage
from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from .forms import SearchForm
from app.server.models import Server
from app.shop.models import Shop
from app.endpoint.models import Network


def paginate_results(results, get_data, paginate_by=25):
    paginator = Paginator(results, paginate_by)
    page_number = get_data.get('page', 1)
    try:
        page = paginator.page(page_number)
    except InvalidPage:
        raise Http404('No such page!')
    return page


def search(request):
    form = SearchForm(data=request.GET or None)
    if form.is_valid():
        visible_products = products_with_details(request.user)
        results = form.search(model_or_queryset=visible_products)
        query = form.cleaned_data.get('q', '')
    else:
        results = []
        query = ''
    page = paginate_results(results, request.GET, settings.PAGINATE_BY)
    ctx = {
        'query': query,
        'results': page,
        'query_string': '?q=%s' % query}
    return render(request, 'search/results.html', ctx)


def shop_search(request):
    form = SearchForm(data=request.GET or None)
    if form.is_valid():
        shops = Shop.objects.all()
        results = form.search(model_or_queryset=shops)
        query = form.cleaned_data.get('q', '')
    else:
        results = []
        query = ''
    print results
    page = paginate_results(results, request.GET, settings.PAGINATE_BY)
    ctx = {
        'query': query,
        'shops': page,
        'query_string': '?q=%s' % query}
    return render(request, 'urpsm/v2/search/shop_search_result_v2.html', ctx)