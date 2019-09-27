from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import *
from .models import *
from customer.models import Profile
from django.views.generic import (UpdateView,DeleteView)
from django.contrib.auth.mixins import (LoginRequiredMixin,UserPassesTestMixin)
from django.contrib.messages.views import SuccessMessageMixin

# Create your views here.
@login_required
def admin_home(request):
    return render(request,'adminHome.html')


# ###################################### agent management ##########################################################
def user_management(request):
    profiles=Profile.get_agents()

    return render(request,'agent/agentManagement.html',{'profiles':profiles}) 


def create_agent(request):

    if request.method=='POST':
        form=AgentCreationForm(request.POST)

        if form.is_valid():
            form.save()

            username=form.cleaned_data.get('username')
            useremail=form.cleaned_data.get('email')
            userphonenumber=form.cleaned_data.get('phonenumber')

            createdAgent=User.objects.filter(email=useremail).first()
            createdAgent.profile.is_staff=True
            createdAgent.profile.phonenumber=userphonenumber
            createdAgent.save()

            messages.success(request,f'Account created for Agent {username}')
            return redirect('user_management')
    else:

        form=AgentCreationForm()
    return render(request,'agent/createAgent.html',{'form':form})     