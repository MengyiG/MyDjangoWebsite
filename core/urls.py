from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # This is a dynamic URL that will take a string as a parameter
    path('channel/<str:pk>/', views.channel, name='channel'),

    path('create-channel/', views.createChannel, name='create-channel'),
    path('update-channel/<str:pk>/', views.updateChannel, name='update-channel'),
]
