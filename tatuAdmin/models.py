from django.db import models
from django.contrib.auth.models import User
from django.db import models
from PIL import Image
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class TicketType(models.Model):
    Critical = 1
    High = 2
    Normal = 3
    Low = 4
    Very_Low=5


    PRIORITY_CHOICES=(
        (Critical,'1. Critical'),
        (High,'2. High'),
        (Normal,'3. Normal'),
        (Low,'4. Low'),
        (Very_Low,'5. Very Low'),
    )

    name=models.CharField(max_length=15,unique=True)
    priority=models.IntegerField(
        choices=PRIORITY_CHOICES,
        default=3,
        blank=3,
        
    )

    def __str__(self):
        return self.name

    @classmethod
    def get_ticket_types(cls):
        tickets=cls.objects.all()
        return tickets  

    @classmethod
    def delete_ticket(cls,pk):
        ticket=cls.objects.get(pk=pk)
        ticket.delete()
             

class TicketSubType(models.Model):
    subtype=models.CharField(max_length=15,unique=True)
    ticket=models.ForeignKey(TicketType,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return f'{self.subtype} Subtype'



class Department(models.Model):
    department_name=models.CharField(max_length=30)
    department_description=models.TextField(max_length=200,blank=True)

    def __str__(self):
        return f'{self.department_name} Department'

    @classmethod
    def get_departments(cls):
        departments=cls.objects.all()
        return departments   
