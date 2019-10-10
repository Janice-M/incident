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
from django.utils import timezone
from django.utils.crypto import get_random_string


from django.contrib.auth import login,authenticate,update_session_auth_hash
from django.contrib.sites.shortcuts import (get_current_site)
from django.utils.encoding import force_bytes,force_text
from django.utils.http import (urlsafe_base64_encode, urlsafe_base64_decode)
from django.template.loader import render_to_string
from customer.tokens import account_activation_token
from django.core.mail import EmailMessage
from django.http import HttpResponse,Http404,HttpResponseRedirect
from customer.forms import UserUpdateForm,ProfileUpdateForm
from django.views import View
from django.contrib.auth.forms import PasswordChangeForm


# Create your views here.
@login_required
def admin_home(request):
    tickets = Create_ticket.get_tickets()
    closed_tickets=Create_ticket.get_closed_tickets()
    pending_tickets=Create_ticket.get_pending_tickets()
    return render(request,'adminHome.html',{'tickets' : tickets ,'closed_tickets':closed_tickets,'pending_tickets':pending_tickets})
##################Customized foe the display of tables #########

@login_required
def tables(request):
    # tickets = Create_ticket.get_tickets()
    closed_tickets=Create_ticket.get_closed_tickets()
    pending_tickets=Create_ticket.get_pending_tickets()
    return render(request,'tables.html',{ 'closed_tickets':closed_tickets,'pending_tickets':pending_tickets})



@login_required
def admin_profile(request):
    if request.method=='POST':
        usrForm=UserUpdateForm(request.POST,instance=request.user)
        profForm=ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        if usrForm.is_valid() and profForm.is_valid():
            usrForm.save()
            profForm.save()

            messages.success(request,'Your account has been updated!')
            return redirect('admin_home')
    else:
        usrForm=UserUpdateForm(instance=request.user)
        profForm=ProfileUpdateForm(instance=request.user.profile)

    context={
        'usrForm':usrForm,
        'profForm':profForm,

    }
    return render(request,'tatuadmin/admin_profile.html',context)

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
        data=request.POST.copy()
        data['password1']=get_random_string(20)

        form=AgentCreationForm(data)

        if form.is_valid():
            agent_form=form.save(commit=False)
            agent_form.is_active=False
            

            username=form.cleaned_data.get('username')
            useremail=form.cleaned_data.get('email')
            userphonenumber=form.cleaned_data.get('phonenumber')
            userpass=form.cleaned_data.get('password1')
            

            try:
                if User.objects.get(email=useremail):

                    messages.warning(request,f'Email already in use with another account')
                    return render(request,'agent/createAgent.html',{'form':form})

                elif Profile.objects.filter(phone_number=userphonenumber).exists():
                    messages.warning(request,f'Phone number already in use with another account')
                    return render(request,'agent/createAgent',{'form':form})


            except ObjectDoesNotExist:
                agent_form.save()

                current_site=get_current_site(request)
                mail_subject='Activate your Agent Account.'
                message=render_to_string('agent/account_email_activate.html',{
                    'user':agent_form,
                    'domain':current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(agent_form.pk)),
                    'token':account_activation_token.make_token(agent_form),
                    'password':userpass,
                    'email':form.cleaned_data.get('email'),
                    'username':username,

                })

                to_email=useremail
                email=EmailMessage(mail_subject,message,to=[to_email])
                email.send()

                createdUser=User.objects.filter(email=useremail).first()
                createdUser.profile.phone_number=userphonenumber
                createdUser.profile.is_staff=True
                createdUser.profile.is_customer=False
                createdUser.profile.date_created=timezone.now()
                createdUser.save()

                messages.success(request,f'Account created for {username} created!')
                return redirect('user_management')

    else:
        form=AgentCreationForm()

    return render(request,'agent/createAgent.html',{'form':form})

class Activate(View):
    '''
    cbv to activate an agent and prompt for a passoword reset
    '''
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
        
            user.is_active = True
            user.save()
            login(request, user)

            form = PasswordChangeForm(request.user)
            return render(request, 'activation.html', {'form': form})

        else:
            return HttpResponse('Activation link is invalid!')

    def post(self, request,*args,**kwargs):
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user) # Important, to update the session with the new password
            messages.success('Password changed successfully')
        return redirect('login')



@login_required
def edit_agent(request,pk):
    agent=User.objects.get(pk=pk)
    if request.method=='POST':
        form=AgentProfileEditForm(request.POST,instance=agent.profile)
        usrform=AgentUpdateForm(request.POST,instance=agent)

        if form.is_valid() and usrform.is_valid():
            profile=form.save(commit=False)
            if profile.is_staff==False:
                agent.is_active=False
                profile.save()
            else:
                agent.is_active=True
                profile.save()

            usrform.save()
            messages.success(request,f'Account Updated for Agent {agent.username}')
            return redirect('user_management')
    else:

        form=AgentProfileEditForm(instance=agent.profile)
        usrform=AgentUpdateForm(instance=agent)
    return render(request,'agent/editAgent.html',{'form':form,'usrform':usrform})


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

            department=form.cleaned_data.get('department_name')
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
    # render ticket types
    tickets=TicketType.get_ticket_types()

    return render(request,'ticket/ticketManagement.html',{'tickets':tickets})


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
def assign_ticket(request, pk):
    '''
    view function to assign a ticket to an agent
    '''
    ticket=Create_ticket.objects.get(pk=pk)
    current_user=request.user
    if request.method=='POST':
        form=AssignForm(request.POST, instance=ticket)

        if form.is_valid():
            take_form=form.save(commit=False)
            if take_form.agent:

                take_form.status=Create_ticket.Pending
                take_form.last_updated=timezone.now()
                take_form.is_taken=True
                take_form.save()
                messages.success(request,f'Ticket {take_form.status} has changed from open to pending!')

            elif take_form.department:
                take_form.last_updated=timezone.now()
                take_form.is_taken=False
                take_form.save()
                messages.success(request,f'Ticket has been assigned to {take_form.department}!')
           
            return redirect('admin_home')

    else:
        form=AssignForm(instance=ticket)

    return render(request,'agent/assign_ticket.html',{'form':form,'ticket':ticket})

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
