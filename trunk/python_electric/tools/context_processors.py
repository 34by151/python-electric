
def menu(request):
    path = request.path.strip('/')
    path = path.split('/')

    topmenu = [['home', '/', False],
               ['about', '/about', False],
               ['contact', '/contact', False],
               ['portfolio', '/portfolio', False],
              ]
	           
    for item in topmenu:
        if item[1].replace('/','') == path[0]:
            item[2] = True
   
    return {'menu':topmenu}       

def settings(request):
    from django.conf import settings as _settings
    return {'settings': _settings}
