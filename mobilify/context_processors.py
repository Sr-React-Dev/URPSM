from settings import GOOGLE_MAP_KEY

def get_request_lang(request):
	return {'LANGUAGE_CODE':request.LANGUAGE_CODE}

def googlemap_key(request):
	return {'GOOGLE_MAP_KEY': GOOGLE_MAP_KEY}