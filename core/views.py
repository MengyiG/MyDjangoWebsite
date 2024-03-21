from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Channel
from .forms import ChannelForm


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
    form = ChannelForm()
    if request.method == 'POST':
        form = ChannelForm(request.POST)
        form = ChannelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'core/channel_form.html', context)


def updateChannel(request, pk):
    channel = Channel.objects.get(id=pk)

    # pass the instance to the form
    form = ChannelForm(instance=channel)

    if request.method == 'POST':
        form = ChannelForm(request.POST, instance=channel)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'core/channel_form.html', context)


def deleteChannel(request, pk):
    channel = Channel.objects.get(id=pk)
    if request.method == 'POST':
        channel.delete()
        return redirect('home')
    return render(request, 'core/delete.html', {'obj': channel})
