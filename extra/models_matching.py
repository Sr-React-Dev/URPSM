    import codecs
    phones = codecs.open('models.txt', 'a')
    from app.phone.models import Model
    modeles = Model.objects.all()
    # print len(models)
    for model in modeles:
       print "poke"
       m =  "%s,%s,%s\n" % (model.brand, model.name, model.pk)
       print m
       phones.write(m)
    phones.close()
