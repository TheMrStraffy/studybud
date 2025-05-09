from django.shortcuts import render
from django.http import HttpResponse
from .models import Room

# Create your views here.

# rooms = [
#     {'id' : 1, 'name' : 'lets learn python!'},
#     {'id' : 2, 'name' : 'lets learn Java!'},
#     {'id' : 3, 'name' : 'lets learn C++!'},
# ]

def home(request):
    getAllRooms = Room.objects.all()
    context = {
        'rooms' : getAllRooms
    }
    return render(request, 'base/home.html', context)

def room(request, pk):
    
    room = Room.objects.get(id=pk)
    
    context = {
        'room' : room
    }
    
    return render(request, 'base/room.html', context)

def createRoom(request):
    context = {}
    return render(request, 'base/room_form.html', context)