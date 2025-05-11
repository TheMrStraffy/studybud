from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpRequest
from .models import Room, Topic
from .forms import RoomForm

# Create your views here.

# rooms = [
#     {'id' : 1, 'name' : 'lets learn python!'},
#     {'id' : 2, 'name' : 'lets learn Java!'},
#     {'id' : 3, 'name' : 'lets learn C++!'},
# ]

def home(request:HttpRequest):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    # With Q imported from django.db.models we can set more parameters to search with
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q)
        ) 
    
    topics = Topic.objects.all()
    room_count = rooms.count()

    context = {
        'rooms' : rooms,
        'room_count' : room_count,
        'topics' : topics
    }
    return render(request, 'base/home.html', context)

def room(request, pk):
    
    room = Room.objects.get(id=pk)
    
    context = {
        'room' : room
    }
    
    return render(request, 'base/room.html', context)

def createRoom(request : HttpRequest):
    form = RoomForm()

    if request.method == 'POST':
        # print(request.POST)
        # print(request.POST.get('host'))
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form' : form}
    return render(request, 'base/room_form.html', context)

def updateRoom(request: HttpRequest, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')


    context = {'form' : form}
    return render(request, 'base/room_form.html', context)

def deleteRoom(request:HttpRequest, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete-room.html', {'obj' : room})