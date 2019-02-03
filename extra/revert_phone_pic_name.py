# from easy_thumbnails.templatetags.thumbnail import thumbnail_url
from easy_thumbnails.files import get_thumbnailer
from app.phone.models import Model
from mobilify.settings import THUMBNAIL_ALIASES, MEDIA_ROOT
from mobilify.utils import PrintException
# import os

model_alias = THUMBNAIL_ALIASES['']['model']
print model_alias

default = "icons/default_phone.png"

thumbnail_options = {'crop': False,'size':(200, 160)}

models = Model.objects.all()


print "Start reverting thumbnails for brands models"

for model in models:
    try:
        if not model.picture ==  default:
            thumbnailer = get_thumbnailer(model.picture)
            filename =  thumbnailer.get_thumbnail_name(thumbnail_options)
            filename = filename.split('.200x160')[0]
            filename = filename.replace('\\', '/')
            model.picture = filename
            model.save()
            

    except:
        PrintException()
    
print "Reverting thumbnails for brands models FINISHED"
