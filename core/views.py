from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Channel, Topic, Message
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import ChannelForm
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.http import HttpResponse


def loginPage(request):

    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        # get the username and password from the form
        username = request.POST.get('username').lower()
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

    context = {'page': page}
    return render(request, 'core/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):

    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # save the user to the database
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            # get the username from the form
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + username)
            # add the user to the session
            login(request, user)
            return redirect('home')
        else:
            messages.error(
                request, 'An error has occurred during registration')

    context = {'form': form}
    return render(request, 'core/login_register.html', context)


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
    # display the messages of the searched channel only
    channel_messages = Message.objects.filter(
        Q(channel__topic__name__icontains=q))

    context = {
        'channels': channels,
        'topics': topics,
        'channel_count': channel_count,
        'channel_messages': channel_messages
    }
    return render(request, 'core/home.html', context)


def channel(request, pk):
    # get the channel from the database and pass it to the template
    channel = Channel.objects.get(id=pk)
    channel_messages = channel.message_set.all()
    # sort the participants alphabetically
    # TODO: why super user is not sorted?
    participants = channel.participants.all().order_by('username')

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            channel=channel,
            body=request.POST.get('body')
        )
        channel.participants.add(request.user)
        # redirect to the same page
        return redirect('channel', pk=channel.id)
    context = {
        'channel': channel, 'channel_messages': channel_messages.order_by('-created'), 'participants': participants
    }
    return render(request, 'core/channel.html', context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    channels = user.channel_set.all()
    channel_messages = user.message_set.all()
    topics = Topic.objects.all()

    context = {'user': user, 'channels': channels,
               'channel_messages': channel_messages, 'topics': topics}
    return render(request, 'core/profile.html', context)


@login_required(login_url='login')
def createChannel(request):
    form = ChannelForm()

    if request.method == 'POST':
        form = ChannelForm(request.POST)
        if form.is_valid():
            channel = form.save(commit=False)
            channel.host = request.user
            channel.save()
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


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        message.delete()
        # TODO: redirect to the previous page
        return redirect('home')
    return render(request, 'core/delete.html', {'obj': message})
