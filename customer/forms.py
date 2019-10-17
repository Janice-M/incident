from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from tatuAdmin.models import *

class UserRegistrationForm(UserCreationForm):
    email=forms.EmailField()
    phonenumber=forms.CharField(max_length=16)

    class Meta:
        model=User
        fields=['username','email','phonenumber','password1','password2']


class UserUpdateForm(forms.ModelForm):
    email=forms.EmailField()

    class Meta:
        '''
            update username and email
        '''
        model=User
        fields=['username','email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['profile_photo','phone_number',]

class CreateTicketForm(forms.ModelForm):
    class Meta:
        model=Create_ticket
        fields=['ticket_subtype','summary',]

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['ticket_subtype'].label='Title'

    #     if 'ticket_type_id' in self.data:
    #         try:
    #             type_id=int(self.data.get('ticket_type_id'))
    #             self.fields['ticket_subtype']=TicketSubType.objects.filter(ticket=type_id).all()
    #         except (ValueError,TypeError):
    #             pass
    #     elif self.instance.pk:
    #         type_id=int(self.data.get('ticket_type_id'))
    #         self.fields['ticket_subtype'].queryset=TicketSubType.objects.filter(ticket=type_id).all()
