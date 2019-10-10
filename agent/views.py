from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from tatuAdmin import views as tatuAdmin_views
from customer.models import Create_ticket
from .forms import *
from django.utils import timezone
from customer.forms import UserUpdateForm,ProfileUpdateForm
from .status_email import send_status_email
# Create your views here.


@login_required
def agent_home(request):
    current_user=request.user
    tickets = Create_ticket.get_tickets()
    closed_tickets=Create_ticket.get_closed_tickets()
    pending_tickets=Create_ticket.get_pending_tickets()
    my_tickets=Create_ticket.get_agent_tickets(current_user)
    return render(request, 'agent/index.html' ,{'tickets' : tickets ,'closed_tickets':closed_tickets,'pending_tickets':pending_tickets,'my_tickets':my_tickets})

def profile(request):
    if request.method=='POST':
        usrForm=UserUpdateForm(request.POST,instance=request.user)
        profForm=ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        if usrForm.is_valid() and profForm.is_valid():
            usrForm.save()
            profForm.save()

            messages.success(request,'Your account has been updated!')
            return redirect('index')
    else:
        usrForm=UserUpdateForm(instance=request.user)
        profForm=ProfileUpdateForm(instance=request.user.profile)

    context={
        'usrForm':usrForm,
        'profForm':profForm,

    }
    return render(request,'agent/profile.html',context)

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
            take_form.last_updated=timezone.now()
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
    department_tickets=Create_ticket.get_tickets_by_department(current_user.profile.department)

    return render(request,'agent/my_tickets.html',{'tickets':tickets,'department_tickets':department_tickets})



@login_required
def resolve_ticket(request,pk):
    '''
    view function for resolving a ticket
    '''
    ticket=Create_ticket.objects.get(pk=pk)
    current_user=request.user
    if request.method=='POST':
        form=ResolveTicketForm(request.POST, instance=ticket)

        if form.is_valid():
            resolve_form=form.save(commit=False)
            if resolve_form.status==Create_ticket.Open:

                resolve_form.is_taken=False
                resolve_form.last_updated=timezone.now()
                resolve_form.agent=None
                resolve_form.save()

                send_status_email(ticket.owner.username,ticket.owner.email,ticket.ticket_number,ticket.get_status_display)

                messages.success(request,f'Ticket {resolve_form.issue} has change from pending to Open !')
                return redirect('my_tickets')

            elif resolve_form.status==Create_ticket.Closed:

                resolve_form.is_taken=False
                resolve_form.agent=request.user
                resolve_form.save()

                send_status_email(ticket.owner.username,ticket.owner.email,ticket.ticket_number,ticket.status)

                messages.success(request,f'Ticket {resolve_form.issue} has change from pending to Closed !')
                return redirect('my_tickets')


    else:
        form=ResolveTicketForm(instance=ticket)

    return render(request,'agent/resolve_ticket.html',{'form':form})
