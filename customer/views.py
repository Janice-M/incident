from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegistrationForm,UserUpdateForm,ProfileUpdateForm,CreateTicketForm
from django.contrib.auth.decorators import login_required
from tatuAdmin import views as tatuAdmin_views
from agent import views as agent_views
from .models import Create_ticket
from .generator import randomStringDigits



def register(request):
# Create your views here.
    '''
    view function for registering
    '''
    if request.method=='POST':
        form=UserRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            useremail=form.cleaned_data.get('email')
            userphonenumber=form.cleaned_data.get('phonenumber')

            createdUser=User.objects.filter(email=useremail).first()
            createdUser.profile.phone_number=userphonenumber
            createdUser.save()

            messages.success(request,f'Account for {username} created!')
            return redirect('login')

    else:
        form=UserRegistrationForm()

    return render(request,'registration/registration_form.html',{'form':form})

@login_required
def index(request):
    '''
    view to redirect the user to their specific dashboard
    '''

    current_user=request.user
    if current_user.is_superuser and current_user.is_staff==True:

        return redirect(tatuAdmin_views.admin_home)
    elif current_user.profile.is_staff==True and current_user.profile.is_customer==False:
        return redirect(agent_views.index)

    else :
        tickets=Create_ticket.get_my_tickets(request.user)
        return render(request,'index.html',{'tickets':tickets})

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
