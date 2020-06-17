from django.http import HttpResponse
 
 
def start(request):
    response = HttpResponse()
    response.write('<h2>Kochamwodę API</h2>')
    response.write('<a href="https://kochamwode.pl">główna</p>')
    return response