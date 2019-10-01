from django.contrib.auth.models import User
from django import forms
from customer.models import Create_ticket

class Take_or_Assign_Form(forms.ModelForm):
    class Meta:
        model=Create_ticket
        fields=['ticket_type','agent']


class ResolveTicketForm(forms.ModelForm):
    class Meta:
        model=Create_ticket
        fields=['status']
