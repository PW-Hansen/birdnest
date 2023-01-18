from django.urls import path
from . import views

urlpatterns = [
    path('', views.live, name = "Wall of Shame"),
    path('manual/', views.home, name = "Testing grounds")
]