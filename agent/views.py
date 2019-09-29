from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from tatuAdmin import views as tatuAdmin_views
from customer.models import Create_ticket
from .forms import *
# Create your views here.

@login_required
def agent_home(request):
    tickets = Create_ticket.get_tickets()
    return render(request, 'agent/index.html' ,{'tickets' : tickets })


@login_required
def take_or_assign_ticket(request, pk):
    '''
    view function for taking or asignong a ticket
    '''
    ticket=Create_ticket.objects.get(pk=pk)
    current_user=request.user
    if request.method=='POST':
        form=Take_or_Assign_Form(request.POST, instance=ticket)

        if form.is_valid():
            take_form=form.save(commit=False)
            take_form.status=Create_ticket.Pending
            take_form.is_taken=True
            take_form.save()


            messages.success(request,f'Ticket {take_form.status} has change from open to pending!')
            return redirect('agent_home')

    else:
        form=Take_or_Assign_Form(instance=ticket)

    return render(request,'agent/take_or_assign.html',{'form':form})



@login_required
def my_tickets(request):
    '''
    view to redirect the agents to their specific tickets
    '''

    current_user=request.user
    tickets=Create_ticket.get_agent_tickets(request.user)

    return render(request,'agent/my_tickets.html',{'tickets':tickets})
@login_required
def create_ticket(request):
    '''
    view function for creating a ticket
    '''
    current_user=request.user
    if request.method=='POST':
        form=CreateTicketForm(request.POST)

        if form.is_valid():
            ctform=form.save(commit=False)
            ctform.status=Create_ticket.Open
            ctform.owner=current_user
            issue=form.cleaned_data.get('issue')
            val=randomStringDigits()
            ctform.ticket_number=str(current_user.id)+val+str(current_user.profile.phone_number)

            ctform.save()


            messages.success(request,f'Your {issue} has been recieved!')
            return redirect('index')

    else:
        form=CreateTicketForm()

    return render(request,'tickets/createticket.html',{'form':form})
