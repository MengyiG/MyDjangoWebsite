from django.shortcuts import render
from django.http import HttpResponse
from .models import Channel


def home(request):
    channels = Channel.objects.all()
    context = {
        'channels': channels
    }
    return render(request, 'core/home.html', context)


def channel(request, pk):
    # get the channel from the database and pass it to the template
    channel = Channel.objects.get(id=pk)
    context = {
        'channel': channel
    }
    return render(request, 'core/channel.html', context)


def createChannel(request):
    context = {}
    return render(request, 'core/channel_form.html', context)
