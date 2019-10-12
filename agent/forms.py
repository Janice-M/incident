from django.contrib.auth.models import User
from django import forms
from customer.models import Create_ticket

class Take_or_Assign_Form(forms.ModelForm):
    u=User.objects.filter(profile__is_customer=False).all()
    agent=forms.ModelChoiceField(queryset=u, empty_label="(Nothing)")

    class Meta:
        model=Create_ticket
        fields=['agent']


class ResolveTicketForm(forms.ModelForm):
    class Meta:
        model=Create_ticket
        fields=['status']

class CreateTicketForCustomerForm(forms.ModelForm):
    customers=User.objects.filter(profile__is_customer=True).all()
    customer=forms.ModelChoiceField(queryset=customer, empty_label="(Nothing)",required=True)
    class Meta:
        model=Create_ticket
        fields=['ticket_subtype','summary','customer'] 

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['ticket_subtype'].label='Title'        
