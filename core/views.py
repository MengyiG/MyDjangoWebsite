from django.shortcuts import render
from django.http import HttpResponse
from .models import Room


def home(request):
    rooms = Room.objects.all()
    context = {
        'rooms': rooms
    }
    return render(request, 'core/home.html', context)


def room(request, pk):
    # get the room from the database and pass it to the template
    room = Room.objects.get(id=pk)
    context = {
        'room': room
    }
    return render(request, 'core/room.html', context)
