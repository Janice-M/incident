from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField
from django.db import models
from .models import *
from customer.models import Profile


class AgentCreationForm(UserCreationForm):
    email=forms.EmailField()
    phonenumber=forms.CharField(max_length=16)

    class Meta:
        model=User
        fields=['username','email','phonenumber','password1','password2']


class AgentEditForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['is_staff','department','phone_number']    



####################################department#######################################

class CreateDepartmentForm(forms.ModelForm): 
    class Meta:
        model=Department
        fields='__all__'    


class DepartmentEditForm(forms.ModelForm):
    class Meta:
        model=Department
        fields='__all__'
 

####################################tickets#######################################

class CreateTicketTypeForm(forms.ModelForm): 
    class Meta:
        model=TicketType
        fields='__all__'    

class EditTicketTypeForm(forms.ModelForm):
    class Meta:
        model=TicketType
        fields='__all__' 


class CreateTicketSubtype(forms.ModelForm): 
    class Meta:
        model=TicketSubType
        fields=['subtype'] 

class CreateMoreTicketSubtype(forms.ModelForm): 
    class Meta:
        model=TicketSubType
        fields='__all__' 
