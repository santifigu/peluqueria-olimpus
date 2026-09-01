from django.shortcuts import render  # type: ignore

# Create your views here.

def index(request):
    return render(request, 'core/index.html')

def politica(request):
    return render(request, 'core/politica.html')