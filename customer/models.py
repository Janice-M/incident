from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from tatuAdmin.models import *
from django.utils import timezone
from django.db.models import Q


# Create your models here.

class Profile(models.Model):
    '''
    '''
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_photo=models.ImageField(upload_to='profile_pics',default='default_profile.png',blank=True)
    phone_number=models.CharField(unique=True,blank=False,null=True,max_length=16)
    department=models.ForeignKey(Department,on_delete=models.DO_NOTHING,null=True,blank=True)
    is_staff = models.BooleanField(default=False,null=True)
    is_customer = models.BooleanField(default=True,null=True)


    def __str__(self):
        return f'{self.user.username} Profile'

    @classmethod
    def get_agents(cls):
        agents=cls.objects.filter(is_customer=False).filter(user__is_superuser=False).all()
        return agents

    @classmethod
    def get_customers(cls):
        customers=cls.objects.filter(is_customer=True).all()
        return customers



    def save(self,*args,**kwargs):
        '''
            overriding the save method of the profile method to resize images

            careful now...make sure the intergrity of the method is retained lest everything collapses
        '''
        super(Profile,self).save(*args,**kwargs)
        img=Image.open(self.profile_photo.path)

        if img.height > 300 or img.width > 300:
            output_size=(300,300)
            img.thumbnail(output_size)
            img.save(self.profile_photo.path)

class Create_ticket(models.Model):
    '''
    '''
    Open = 0
    Pending = 1
    Closed = 2

    Statuses=(
       (Open,'Open'),
       (Pending,'Inprogress'),
       (Closed,'Closed'),

   )
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name='owner')
    ticket_type=models.ForeignKey(TicketType,on_delete=models.CASCADE,null=True)
    ticket_subtype=models.ForeignKey(TicketSubType,on_delete=models.CASCADE)
    status=models.IntegerField(choices=Statuses,default=0,blank=0)
    agent = models.ForeignKey(User,null=True,on_delete=models.DO_NOTHING,related_name='agent',blank=True)
    issue = models.CharField(max_length=60,blank=True,null=True)
    summary = models.TextField(max_length=120,blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(default=timezone.now)
    ticket_number = models.CharField(max_length=100,blank=True,null=True)
    is_taken = models.BooleanField(default=False,null=True)
    department=models.ForeignKey(Department,on_delete=models.DO_NOTHING,null=True,blank=True)

    def __str__(self):
        return f'{self.owner.username}{self.issue}'

    @classmethod
    def get_my_tickets(cls,owner):
        my_tickets=cls.objects.filter(owner=owner).all()
        return my_tickets

    @classmethod
    def get_tickets(cls):

        tickets=cls.objects.filter(is_taken=False).filter(status=cls.Open).all()
        return tickets

    @classmethod
    def get_closed_tickets(cls):

        tickets=cls.objects.filter(status=cls.Closed).all()
        return tickets

    @classmethod
    def get_pending_tickets(cls):

        tickets=cls.objects.filter(status=cls.Pending).all()
        return tickets

    @classmethod
    def get_agent_tickets(cls,agent):
        tickets=cls.objects.filter(agent=agent).all()
        return tickets

    @classmethod
    def get_tickets_by_department(cls,department):
        tickets=cls.objects.filter(status=cls.Open).filter(department=department).all()
        return tickets    

    @classmethod
    def search_my_tickets(cls,owner,search_term):
        ticket=cls.objects.filter(owner=owner).filter(Q(issue__icontains=search_term) |Q(ticket_number__icontains=search_term)|Q(summary__icontains=search_term)|Q(ticket_subtype__subtype__icontains=search_term))
        return ticket

    @classmethod
    def search_all_tickets(cls,search_term):
        tickets=cls.objects.filter(Q(issue__icontains=search_term) |Q(ticket_number__icontains=search_term)|Q(summary__icontains=search_term)|Q(ticket_subtype__subtype__icontains=search_term))
        return tickets
