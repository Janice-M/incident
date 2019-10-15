from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from tatuAdmin import views as tatuAdmin_views
from customer.models import Create_ticket
from tatuAdmin.models import *
from customer.generator import randomStringDigits
from .forms import *
from django.utils import timezone
from customer.forms import UserUpdateForm,ProfileUpdateForm
from .status_email import send_status_email
from django.contrib.auth import login,authenticate,update_session_auth_hash
from django.contrib.auth.forms import SetPasswordForm
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


def agent_change_password(request):
    '''
    function to change a password for an agent
    '''
    if request.method=='POST':
        form=SetPasswordForm(request.user,request.POST)
        if form.is_valid():
            user=form.save()
            update_session_auth_hash(request,user)
            messages.success(request,'Your password was successfully updated')
            return redirect('agent_home')
        else:
            messages.error(request,'Please correct the error below.')
    else:
        form=SetPasswordForm(request.user)
    return render(request,'agent/change_password.html',{'form':form})

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

    return render(request,'agent/take_or_assign.html',{'form':form,'ticket':ticket})


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



@login_required
def create_ticket_for_customer(request):
    '''
    view function for creating a ticket for a customer
    '''
    current_user=request.user
    if request.method=='POST':
        form=CreateTicketForCustomerForm(request.POST)

        if form.is_valid():
            ctform=form.save(commit=False)

            # <class 'tatuAdmin.models.TicketSubType'>
            subtype=form.cleaned_data.get('ticket_subtype')

            #subtype.subtype is the the str name for the subtype.Here we are fetching the ticket type
            ticket_type=TicketSubType.objects.filter(subtype=subtype.subtype).first().ticket
            ctform.ticket_type=ticket_type
            
            owner_class=form.cleaned_data.get('customer')
            customer=User.objects.filter(username=owner_class.username).first()
            ctform.owner=customer

            ctform.status=Create_ticket.Open
    
            val=randomStringDigits()
            ctform.ticket_number=str(current_user.id)+val

            ctform.save()
            mssg=f'Ticket created for customer {customer.username}'

            messages.success(request,mssg)
            return redirect('agent_home')

    else:
        form=CreateTicketForCustomerForm()

    return render(request,'agent/create_ticket_for_customer.html',{'form':form})


def search_tickets(request):
    current_user=request.user
    if 'ticket' in request.GET and request.GET['ticket']:

        search_term=request.GET.get('ticket')
        ticketi=Create_ticket.search_all_tickets(search_term)

        context={
        'message':f"{search_term}",
        'ticket':ticketi
        }
        
        return render(request,'agent/search.html',context)

    else :

        context={
        'message':"Sorry, but the ticket seems not to exist or the ticket number is incorrect! Please check the ticket number and try again "
        }
    return render(request,'agent/search.html',context)
