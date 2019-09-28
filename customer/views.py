from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegistrationForm,UserUpdateForm,ProfileUpdateForm,CreateTicketForm
from django.contrib.auth.decorators import login_required
from tatuAdmin import views as tatuAdmin_views
from .models import Create_ticket


# Create your views here.
def register(request):
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

    else :
        return render(request,'index.html')

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
            ctform.save()
            

            messages.success(request,f'Your {issue} has been recieved!')
            return redirect('index')

    else:
        form=CreateTicketForm()
    
    return render(request,'tickets/createticket.html',{'form':form})

