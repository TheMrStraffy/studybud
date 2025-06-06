from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpRequest, HttpResponse
from .models import Room, Topic, Message
from .forms import RoomForm, UserForm
from django.views import View

# class ExampleView(View):
#     def get(self, request:HttpRequest):
#         return render(request, 'base/example.html')


# Create your views here.

# rooms = [
#     {'id' : 1, 'name' : 'lets learn python!'},
#     {'id' : 2, 'name' : 'lets learn Java!'},
#     {'id' : 3, 'name' : 'lets learn C++!'},
# ]

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    all_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {
        'user':user,
        'rooms' : rooms,
        'topics' : topics,
        'all_messages':all_messages
        }
    return render(request, 'base/user-profile.html', context)

def loginView(request:HttpRequest):

    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exist')

    context = {
        'page':page
    }
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUserView(request:HttpRequest):
    # page = 'register'
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user : User = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request,'Error occurred during registration...')

    return render(request, 'base/login_register.html', {'form':form})

def home(request:HttpRequest):
    q = request.GET.get('q', '')

    if q:
        rooms = Room.objects.filter(
            Q(topic__name__iexact=q)
        )
        
        all_messages = Message.objects.filter(
            Q(room__topic__name__iexact=q)
        )
    else:
        rooms = Room.objects.all()
        all_messages = Message.objects.all()

    # With Q imported from django.db.models we can set more parameters to search with
    # rooms = Room.objects.filter(
    #     Q(topic__name=q)
    #     ) 
    
    topics = Topic.objects.all()[0:3]
    room_count = rooms.count()


    context = {
        'rooms' : rooms,
        'room_count' : room_count,
        'topics' : topics,
        'all_messages' : all_messages,
    }
    return render(request, 'base/home.html', context)

def room(request:HttpRequest, pk):
    
    room : Room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)

        return redirect('room', pk=room.id)

    context = {
        'room' : room,
        'room_messages' : room_messages,
        'participants' : participants,
    }
    
    return render(request, 'base/room.html', context)


@login_required(login_url='login')
def createRoom(request : HttpRequest):
    form = RoomForm()

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room : Room = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect('home')

    context = {'form' : form}
    return render(request, 'base/room_form.html', context)
 
@login_required(login_url='login')
def updateRoom(request: HttpRequest, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home') 


    context = {'form' : form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request:HttpRequest, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj' : room})

@login_required(login_url='login')
def deleteMessage(request:HttpRequest, pk):
    room_message : Message = Message.objects.get(id=pk)

    if request.user != room_message.user:
        return HttpResponse('Not allowed')

    if request.method == 'POST':
        room_message.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': room_message})

@login_required(login_url='login')
def updateUser(request:HttpRequest):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid:
            form.save()
            return redirect('user-profile', pk=user.id)

    context = {'form' : form}
    return render(request, 'base/update-user.html', context)

def topicsPage(request:HttpRequest):

    q = request.GET.get('q', '')

    if q:
        topics = Topic.objects.filter(name__icontains=q)
    else:
        topics = Topic.objects.all()
        
    context = {'topics' : topics}
    return render(request, 'base/topics.html', context)

def activityPage(request:HttpRequest):
    all_messages = Message.objects.all()
    context = {'all_messages' : all_messages}
    return render(request, 'base/activity.html', context)