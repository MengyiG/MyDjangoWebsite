from django.shortcuts import render, redirect
from .models import Channel, Topic
from .forms import ChannelForm
from django.db.models import Q


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    # get the channels from the database when the topic name contains the query
    # case insensitive
    channels = Channel.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()
    channel_count = channels.count()
    context = {
        'channels': channels,
        'topics': topics,
        'channel_count': channel_count
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
