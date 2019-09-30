from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import *
from .models import *
from customer.models import Create_ticket
from customer.models import Profile
from django.views.generic import (UpdateView,DeleteView)
from django.contrib.auth.mixins import (LoginRequiredMixin,UserPassesTestMixin)
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ObjectDoesNotExist


from django.contrib.auth import login,authenticate
from django.contrib.sites.shortcuts import (get_current_site)
from django.utils.encoding import force_bytes,force_text
from django.utils.http import (urlsafe_base64_encode, urlsafe_base64_decode)
from django.template.loader import render_to_string
from customer.tokens import account_activation_token
from django.core.mail import EmailMessage
from django.http import HttpResponse,Http404,HttpResponseRedirect

# Create your views here.
@login_required
def admin_home(request):
    return render(request,'adminHome.html')


# ###################################### agent management ##########################################################
@login_required
def user_management(request):
    profiles=Profile.get_agents()

    return render(request,'agent/agentManagement.html',{'profiles':profiles}) 

@login_required
def create_agent(request):

    '''
    view function for creating an agent
    '''
    if request.method=='POST':
        form=AgentCreationForm(request.POST)

        if form.is_valid():
            agent_form=form.save(commit=False)
            agent_form.is_active=False
            
						
            username=form.cleaned_data.get('username')
            useremail=form.cleaned_data.get('email')
            userphonenumber=form.cleaned_data.get('phonenumber')
            
            try:
                if User.objects.get(email=useremail):

                    messages.warning(request,f'Email already in use with another account')
                    return render(request,'agent/createAgent.html',{'form':form})

                elif userphonenumber==Profile.objects.filter(phone_number=userphonenumber).first():
                    messages.warning(request,f'Phone number already in use with another account')
                    return render(request,'agent/createAgent',{'form':form})


            except ObjectDoesNotExist:
                form.save()
                
                current_site=get_current_site(request)
                mail_subject='Activate your Agebnt Account.'
                message=render_to_string('agent/account_email_activate.html',{
                    'user':agent_form,
                    'domain':current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(agent_form.pk)),
                    'token':account_activation_token.make_token(agent_form),

                })

                to_email=useremail
                email=EmailMessage(mail_subject,message,to=[to_email])
                email.send()

                createdUser=User.objects.filter(email=useremail).first()
                createdUser.profile.phone_number=userphonenumber
                createdUser.profile.is_staff=True
                createdUser.profile.is_customer=False
                createdUser.save()
                
                messages.success(request,f'Account created for {username} created!')
                return redirect('user_management')

    else:
        form=AgentCreationForm()

    return render(request,'agent/createAgent.html',{'form':form})


@login_required
def edit_agent(request,pk):
    agent=User.objects.get(pk=pk)
    if request.method=='POST':
        form=AgentEditForm(request.POST,instance=agent.profile)

        if form.is_valid():
            form.save()
            messages.success(request,f'Account Updated for Agent {agent.username}')
            return redirect('user_management')
    else:

        form=AgentEditForm(instance=agent.profile)
    return render(request,'agent/editAgent.html',{'form':form}) 


# ###################################### department management ##########################################################
@login_required
def department_management(request):

    departments=Department.get_departments()
    

    return render(request,'department/departmentmanagement.html',{'departments':departments}) 


@login_required
def create_department(request):

    if request.method=='POST':
        form=CreateDepartmentForm(request.POST)

        if form.is_valid():
            form.save()

            department=form.cleaned_data.get('department')
            messages.success(request,f'{department} created successfully')
            return redirect('department_management')
    else:

        form=CreateDepartmentForm()
    return render(request,'department/createDepartment.html',{'form':form})


@login_required
def edit_department(request,pk):
    department=Department.objects.get(pk=pk)
    if request.method=='POST':
        form=DepartmentEditForm(request.POST,instance=department)

        if form.is_valid():
            form.save()
            messages.success(request,f'Department updated successfully')
            return redirect('department_management')
    else:

        form=DepartmentEditForm(instance=department)
    return render(request,'department/editDepartment.html',{'form':form}) 



# ###################################### ticket management ##########################################################
@login_required
def ticket_management(request):

    tickets=TicketType.get_ticket_types()
    all_tickets=Create_ticket.get_tickets()

    return render(request,'ticket/ticketManagement.html',{'tickets':tickets,'all_tickets':all_tickets})     


@login_required
def create_ticket(request):

    if request.method=='POST':
        tform=CreateTicketTypeForm(request.POST)
        tformsub=CreateTicketSubtype(request.POST)

        if tform.is_valid():

            tform.save()
            tformsub.save()

            ticketname=tform.cleaned_data.get('name')
            newlyCreatedTicket=TicketType.objects.filter(name=ticketname).first()

            subtypename=tformsub.cleaned_data.get('subtype')
            newlyCreatedSubtype=TicketSubType.objects.filter(subtype=subtypename).first()

            newlyCreatedSubtype.ticket=newlyCreatedTicket
            newlyCreatedSubtype.save()


            messages.success(request,f'Ticket Type {ticketname} created successfully')
            return redirect('ticket_management')
    else:

        tform=CreateTicketTypeForm(request.POST)
        tformsub=CreateTicketSubtype(request.POST)

    return render(request,'ticket/createTicket.html',{'tform':tform,'tformsub':tformsub}) 


@login_required
def edit_ticket(request,pk):
    ticket=TicketType.objects.get(pk=pk)
    if request.method=='POST':
        form=EditTicketTypeForm(request.POST,instance=ticket)

        if form.is_valid():
            form.save()
            messages.success(request,f'Ticket updated successfully')
            return redirect('ticket_management')
    else:

        form=EditTicketTypeForm(instance=ticket)
    return render(request,'ticket/editTicket.html',{'form':form}) 


class TicketDeleteView(LoginRequiredMixin,SuccessMessageMixin,DeleteView):
    '''
    class view method to delete a ticket
        declare the model to be affected
        declare the template to be used
       
    '''
    model=TicketType
    template_name='ticket/ticketConfirmDelete.html'
    success_url='/'
    success_message = "Ticket was deleted successfully"
  

# ###################################### ticket subtypes ##########################################################
@login_required
def create_ticket_subtypes(request):

    if request.method=='POST':
        subtypesform=CreateMoreTicketSubtype(request.POST)
     
        if subtypesform.is_valid():

            subtypesform.save()
            subtypename=subtypesform.cleaned_data.get('subtype')

            messages.success(request,f'{subtypename} created successfully')
            return redirect('ticket_management')
    else:
        subtypesform=CreateMoreTicketSubtype(request.POST)
    
    return render(request,'ticket/createSubtype.html',{'form':subtypesform})   
