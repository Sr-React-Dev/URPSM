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

models = Model.objects.all()[:60]


print "Start making thumbnails for brands models"

for model in models:
    try:
        if not model.picture ==  default:
            # picture = os.path.join(MEDIA_ROOT, model.picture)

            # print thumbnail_url(model.picture, model_alias)
            # print model.name, "processed"
            thumbnailer = get_thumbnailer(model.picture)
            thumbnailer.get_thumbnail(thumbnail_options)
            thumbnail_name =  thumbnailer.get_thumbnail_name(thumbnail_options)
            _thumbnail_name = thumbnail_name.replace('\\', '/')
            
            if thumbnailer.thumbnail_exists(thumbnail_name):
                if "\\" in thumbnail_name:
                    model.picture = _thumbnail_name
                    model.save()
                    print model.name, thumbnail_name, 'renamed'
                    
            else:
                model.picture = _thumbnail_name
                model.save()
                print model.name, _thumbnail_name , 'created'
        else:
            print model.name , "not concerned"

    except:
        PrintException()
    
print "Making thumbnails for brands models FINISHED"
