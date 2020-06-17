from django.http import HttpResponse, HttpResponseRedirect
from django.urls import resolve


def start(request):
    return HttpResponseRedirect('https://kochamwode.pl/')
    