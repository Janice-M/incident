from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from tatuAdmin import views as tatuAdmin_views
from customer.models import Create_ticket
# Create your views here.
@login_required
def index(request):
    tickets = Create_ticket.get_tickets()
    return render(request, 'index.html' ,{'tickets' : tickets })
