from urllib2 import urlopen
import json
def get_place(latLng, radius):
    url = "http://maps.googleapis.com/maps/api/geocode/json?"
    url += "latlng=%s&sensor=false" % latLng
    v = urlopen(url).read()
    j = json.loads(v)
    # print j
    if not j['status'] == u'ZERO_RESULTS':
        components = j['results'][0]['address_components']
        country = town = admin_area_2 = code = None
        for c in components:
            if "country" in c['types']:
                country = c['long_name']
                code    = c['short_name']
            if "administrative_area_level_2" in c['types']:
                admin_area_2 = c['long_name']
            if "locality" in c['types']:
                town = c['long_name']
            if "sublocality_level_1" in c['types']:
                town = c['long_name']
        # print c
    # print town, admin_area_2, country,code, j['results'][0]
        return town, admin_area_2, country,code, j['results'][0]
    else:
        return (None,None)