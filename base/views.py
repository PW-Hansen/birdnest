from django.shortcuts import render
from django.http import HttpResponse
from .models import Drone, Pilot
from .functions import generate_violating_pilots_string

# Create your views here.

def home(request):
    pilot_string = generate_violating_pilots_string()
    drones = Drone.objects.all()
    pilots = Pilot.objects.all()
    context = {'drones': drones, 'pilots': pilots, 'pilot_string': pilot_string}
    return render(request, 'base/home.html', context)

def live(request):
    context = {}
    return render(request, 'base/live.html', context)