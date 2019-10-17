from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegistrationForm,UserUpdateForm,ProfileUpdateForm,CreateTicketForm
from django.contrib.auth.decorators import login_required
from tatuAdmin import views as tatuAdmin_views
from agent import views as agent_views
from .models import Create_ticket
from tatuAdmin.models import *
from .generator import randomStringDigits
from customer.models import Profile
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth import login,authenticate
from django.contrib.sites.shortcuts import (get_current_site)
from django.utils.encoding import force_bytes,force_text
from django.utils.http import (urlsafe_base64_encode, urlsafe_base64_decode)
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.http import HttpResponse,Http404,HttpResponseRedirect



def register(request):
# Create your views here.
    '''
    view function for registering
    '''
    if request.method=='POST':
        form=UserRegistrationForm(request.POST)

        if form.is_valid():
            rf=form.save(commit=False)
            rf.is_active=False

            username=form.cleaned_data.get('username')
            useremail=form.cleaned_data.get('email')
            userphonenumber=form.cleaned_data.get('phonenumber')

            try:
                if User.objects.get(email=useremail):

                    messages.warning(request,f'Email already in use with another account')
                    return render(request,'registration/registration_form.html',{'form':form})

                # elif Profile.objects.get(phone_number=userphonenumber):

                #     messages.warning(request,f'Phone number already in use with another account')
                #     return render(request,'registration/registration_form.html',{'form':form})


            except ObjectDoesNotExist:
                form.save()

                current_site=get_current_site(request)
                mail_subject='Activate your Tatu Account.'
                message=render_to_string('registration/account_email_activate.html',{
                    'user':rf,
                    'domain':current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(rf.pk)),
                    'token':account_activation_token.make_token(rf),

                })

                to_email=useremail
                email=EmailMessage(mail_subject,message,to=[to_email])
                email.send()

                # user.refresh_from_db()
                createdUser=User.objects.filter(email=useremail).first()
                createdUser.profile.phone_number=userphonenumber
                createdUser.profile.is_customer= True
                createdUser.save()



                messages.success(request,f'Account for {username} created!Please confirm you email to complete registration')
                return redirect('login')

    else:
        form=UserRegistrationForm()

    return render(request,'registration/registration_form.html',{'form':form})



def activate(request, uidb64, token):
    current_user=request.user
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):

        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # checking user type
        if current_user.is_superuser==True:
            from tatuAdmin import views as tatuAdmin_views
            #redirect newly created admin to change their password

            return redirect(tatuAdmin_views.change_password)

        elif current_user.profile.is_staff==True and current_user.profile.is_customer==False:
            from agent import views as agent_views
            # redirect newly created agent to change their password

            return redirect(agent_views.agent_change_password)


        return redirect('index')


    else:
        return HttpResponse('Activation link is invalid!')


@login_required
def index(request):
    '''
    view to redirect the user to their specific dashboard
    '''

    current_user=request.user

    if current_user.is_superuser==True:

        print(current_user.is_superuser,"yeah")
        return redirect(tatuAdmin_views.admin_home)

    elif current_user.profile.is_staff==True and current_user.profile.is_customer==False:
        print(current_user.is_superuser,"agent")
        return redirect(agent_views.agent_home)

    else :
        tickets=Create_ticket.get_my_tickets(request.user)
        return render(request,'customer/index.html',{'tickets':tickets})

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

            # <class 'tatuAdmin.models.TicketSubType'>
            subtype=form.cleaned_data.get('ticket_subtype')

            #subtype.subtype is the the str name for the subtype.Here we are fetching the ticket type
            ticket_type=TicketSubType.objects.filter(subtype=subtype.subtype).first().ticket
            ctform.ticket_type=ticket_type
            print(ticket_type,type(ticket_type),"subtypeeeeeeeeeeeeeeeeeeeee")

            ctform.status=Create_ticket.Open
            ctform.owner=current_user

            val=randomStringDigits()
            ctform.ticket_number=str(current_user.id)+val

            ctform.save()
            mssg=f'{request.user.username} ,Thank You for contacting us.A support ticket request has been created and a representative will be getting back to you shortly if necessary.'

            messages.success(request,mssg)
            return redirect('index')

    else:
        form=CreateTicketForm()

    return render(request,'tickets/createticket.html',{'form':form})

def load_subtypes(request):
    type_id=request.GET.get('ticket_type_id')
    subtypes=TicketSubType.objects.filter(ticket=type_id).all()
    return render(request,'tickets/subtypes_dropdown_list.html',{'subtypes':subtypes})


@login_required
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
    return render(request,'registration/profile.html',context)


def search_issues(request):
    current_user=request.user
    if 'ticket' in request.GET and request.GET['ticket']:

        search_term=request.GET.get('ticket')
        ticketi=Create_ticket.search_my_tickets(current_user,search_term)

        context={
        'message':f"{search_term}",
        'ticket':ticketi
        }

        return render(request,'customer/searches.html',context)

    else :

        context={
        'message':"Sorry, but the ticket seems not to exist or the ticket number is incorrect! Please check the ticket number and try again "
        }
    return render(request,'customer/searches.html',context)
