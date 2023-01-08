from django.shortcuts import render
from django.http import HttpResponse
from .models import Drone
from .functions import update_drones

# Create your views here.

def home(request):
    update_drones()
    drones = Drone.objects.all()
    context = {'drones': drones}
    return render(request, 'base/home.html', context)

def live(request):
    context = {'text': 'This is a test'}
    return render(request, 'base/live.html', context)