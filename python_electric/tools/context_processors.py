
def settings(request):
	from django.conf import settings as _settings
	return {'settings': _settings}
