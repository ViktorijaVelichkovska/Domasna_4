from django.shortcuts import render

def home(request):
    return render(request, 'reactapp/build/index.html')

