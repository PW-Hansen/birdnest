from django.shortcuts import render
from .functions import generate_violating_pilots_string

# Create your views here.

def home(request):
    pilot_string = generate_violating_pilots_string()
    context = {'pilot_string': pilot_string}
    return render(request, 'base/home.html', context)