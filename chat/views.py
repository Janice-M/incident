from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
from django.contrib.auth.decorators import login_required
from .models import Room
# Create your views here.
def index_chat(request):
    return render(request, 'chat/index.html', {})

def room(request, room_name):
    return render(request, 'chat/room.html', {
    'room_name_json': mark_safe(json.dumps(room_name))
    })
@login_required
def index(request):
    """
    Root page view. This is essentially a single-page app, if you ignore the
    login and admin parts.
    """
    # Get a list of rooms, ordered alphabetically
    rooms = Room.objects.order_by("title")

    # Render that in the index template
    return render(request, "index.html", {
        "rooms": rooms,
    })
