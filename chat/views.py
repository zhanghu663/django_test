from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'chat/index.html')


def room(request, group_name):
    return render(request, 'chat/room.html', {
        'room_name': group_name
    })
