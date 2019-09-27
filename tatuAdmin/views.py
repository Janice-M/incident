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
            createdAgent.profile.phone_number=userphonenumber
            createdAgent.save()

            messages.success(request,f'Account created for Agent {username}')
            return redirect('user_management')
    else:

        form=AgentCreationForm()
    return render(request,'agent/createAgent.html',{'form':form})  


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
def department_management(request):

    departments=Department.get_departments()

    return render(request,'department/departmentmanagement.html',{'departments':departments}) 



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

