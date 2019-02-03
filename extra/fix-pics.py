from app.shop.models import Shop
from app.server.models import Server

shops = Shop.objects.all()

for shop in shops:
  if shop.logo == 'default.png':
     shop.logo = 'icons/default_store.png'
     shop.save()

     print shop.name,'logo changed'


print 'All shops logos edited'

servers = Server.objects.all()

for server in servers:
  if server.logo == 'default.png' or server.logo=='icons/default_store.png':
     server.logo = 'icons/default_server.png'
     server.save()

     print server.name,'logo changed'


print 'All servers logos edited'

from app.phone.models import Model


models = Model.objects.all()

for model in models:
    if model.picture == '':
        model.picture = 'icons/default_phone.png'
        model.save()
        print model.name, 'picture changed'

print 'All models pics edited'
