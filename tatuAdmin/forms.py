from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField
from django.db import models
from .models import *
from customer.models import Profile


class AgentCreationForm(UserCreationForm):
    email=forms.EmailField()

    class Meta:
        model=User
        fields=['username','email','password1','password2']


class AgentEditForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['is_staff','department']     
