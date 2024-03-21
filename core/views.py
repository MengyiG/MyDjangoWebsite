from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Channel, Topic
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import ChannelForm
from django.db.models import Q
from django.http import HttpResponse


def loginPage(request):
    if request.method == 'POST':
        # get the username and password from the form
        username = request.POST.get('username')
        password = request.POST.get('password')

        # authenticate the user
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # add the user to the session
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'core/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


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


@login_required(login_url='login')
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


@login_required(login_url='login')
def updateChannel(request, pk):
    channel = Channel.objects.get(id=pk)

    # pass the instance to the form
    form = ChannelForm(instance=channel)

    if request.user != channel.host:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        form = ChannelForm(request.POST, instance=channel)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'core/channel_form.html', context)


@login_required(login_url='login')
def deleteChannel(request, pk):
    channel = Channel.objects.get(id=pk)

    if request.user != channel.host:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        channel.delete()
        return redirect('home')
    return render(request, 'core/delete.html', {'obj': channel})
