from django.conf import settings
def baseurl(request):
    """
    Return a BASE_URL template context for the current request.
    """
    if request.is_secure():
        scheme = 'https://'
    else:
        scheme = 'http://'
        
        return {'BASE_URL': scheme + request.get_host(),}

def sitetitle(request):
    """
    Return a SITE_TITLE template context for the current request.
    """
    try:
        title = settings.SITE_TITLE
    except:
        title = "settings.SITE_TITLE"
            
    return {'SITE_TITLE': title}
