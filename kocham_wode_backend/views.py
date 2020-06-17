from django.http import HttpResponse, HttpResponseRedirect
from django.urls import resolve


def get_root_url(request):
    uri_parts = request.build_absolute_uri().split('.')
    
    return ('.'.join(uri_parts[-2:]) 
            if uri_parts[-1].isalpha() 
            else '')

def start(request):
    return HttpResponseRedirect(get_root_url(request))
    