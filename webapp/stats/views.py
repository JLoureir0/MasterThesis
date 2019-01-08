from django.shortcuts import render
from django.http import HttpResponse

context = {'title': 'Stats'}

def home(request):
    return render(request, 'stats/index.html', context)

def about(request):
    return render(request, 'stats/about.html', context)

