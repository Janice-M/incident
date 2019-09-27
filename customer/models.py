from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from tatuAdmin.models import Department

# Create your models here.

class Profile(models.Model):
    '''
    '''
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_photo=models.ImageField(upload_to='profile_pics',default='default_profile.png',blank=True)
    phone_number=models.CharField(blank=False,null=True,max_length=16)
    department=models.ForeignKey(Department,on_delete=models.DO_NOTHING,null=True,blank=True)
    is_staff = models.BooleanField(default=False,null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    @classmethod
    def get_agents(cls):
        agents=cls.objects.filter(is_staff=True).all()
        return agents
    

    # def save(self,*args,**kwargs):
    #     '''
    #         overriding the save method of the profile method to resize images

    #         careful now...make sure the intergrity of the method is retained lest everything collapses
    #     '''
    #     super(Profile,self).save(*args,**kwargs)
    #     img=Image.open(self.profile_photo.path)

    #     if img.height > 300 or img.width > 300:
    #         output_size=(300,300)
    #         img.thumbnail(output_size)
    #         img.save(self.profile_photo.path) 

