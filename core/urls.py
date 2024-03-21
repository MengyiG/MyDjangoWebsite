from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # This is a dynamic URL that will take a string as a parameter
    path('room/<str:pk>/', views.room, name='room'),
]
