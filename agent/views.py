from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from tatuAdmin import views as tatuAdmin_views
from customer.models import Create_ticket
from .forms import *
# Create your views here.
@login_required
def index(request):
    tickets = Create_ticket.get_tickets()
    return render(request, 'agent/index.html' ,{'tickets' : tickets })

@login_required
def take_or_assign_form(request):
    '''
    view function for taking or asignong a ticket
    '''
    current_user=request.user
    if request.method=='POST':
        form=Take_or_Assign_Form(request.POST)

        if form.is_valid():
            take_form=form.save(commit=False)
            take_form.status=Create_ticket.Pending
            take_form.save()


            messages.success(request,f'Ticket {take_form.status} has change from open to pending!')
            return redirect('index')

    else:
        form=CreateTicketForm()

    return render(request,'tickets/createticket.html',{'form':form})
