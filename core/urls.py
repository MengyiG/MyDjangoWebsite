from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('profile/<str:pk>/', views.userProfile, name='user-profile'),
    path('', views.home, name='home'),

    # This is a dynamic URL that will take a string as a parameter
    path('channel/<str:pk>/', views.channel, name='channel'),

    path('create-channel/', views.createChannel, name='create-channel'),
    path('update-channel/<str:pk>/', views.updateChannel, name='update-channel'),
    path('delete-channel/<str:pk>/', views.deleteChannel, name='delete-channel'),
    path('delete-message/<str:pk>/', views.deleteMessage, name='delete-message'),
]
