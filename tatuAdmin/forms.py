from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField
from django.db import models
from .models import *
from customer.models import *
from django.utils.crypto import get_random_string


class AgentCreationForm(UserCreationForm):
    Admin = 0
    Agent= 1

    roles=(
        (Admin,'1.Administrator'),
        (Agent,'2.Agent'),
    )

    email=forms.EmailField()
    phonenumber=forms.CharField(max_length=16)
    role=forms.ChoiceField(choices=roles,required=True)
 

    class Meta:
        model=User
        fields=['username','email','phonenumber','role','password1','password2']

    # def __init__(self, *args, **kwargs):
    #     super(AgentCreationForm, self).__init__(*args, **kwargs)
    #     self.fields['password1'].required = False
    #     self.fields['password2'].required = False
    #     # If one field gets autocompleted but not the other, our 'neither
    #     # password or both password' validation will be triggered.
    #     del self.fields['password1']
    #     del self.fields['password2']
    
    # def save(self, commit=True):

    #     user =super(UserCreationForm, self).save(commit=False)
    #     user.set_password(self.cleaned_data["password1"])
        
    #     if commit:
    #         user.save()
    #     return user    
        
       


class AgentProfileEditForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['is_staff','department','phone_number']

class AgentUpdateForm(forms.ModelForm):
    email=forms.EmailField()

    class Meta:
        '''
            update username and email
        '''
        model=User
        fields=['username','email']    



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

class AssignForm(forms.ModelForm):
    u=User.objects.filter(profile__is_customer=False).all()
    agent=forms.ModelChoiceField(queryset=u, empty_label="(Nothing)")
    
    class Meta:
        model=Create_ticket
        fields=['ticket_type','agent']

