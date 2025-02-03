from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

def index(request):
    context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}
    return render(request, 'rango/index.html', context_dict)

def about(request):
    context_dict = {
        'message': "This tutorial has been put together by Karla Mihai",
        'MEDIA_URL': settings.MEDIA_URL  # Make sure MEDIA_URL is passed into the context
    }
    return render(request, 'rango/about.html', context_dict)


