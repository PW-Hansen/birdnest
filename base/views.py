from django.shortcuts import render
from django.http import HttpResponse
from . import functions

# Create your views here.

violating_pilots = [
    {'id': 1, 'name': 'peter', 'email': 'peter@mail.com', 'phone': '123456789', 'closest_distance': 50},
    {'id': 2, 'name': 'anders', 'email': 'anders@mail.com', 'phone': '123456789', 'closest_distance': 60},
    {'id': 3, 'name': 'inge', 'email': 'inge@mail.com', 'phone': '123456789', 'closest_distance': 25},
    {'id': 4, 'name': 'niels ole', 'email': 'no@mail.com', 'phone': '123456789', 'closest_distance': 80},
]


def home(request):
    
    context = {'violating_pilots': violating_pilots}
    return render(request, 'base/home.html', context)

def live(request):
    context = {'text': 'This is a test'}
    return render(request, 'base/live.html', context)