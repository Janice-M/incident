#signal fired after an obj is saved in this cas when a user is created
from django.db.models.signals import post_save

#user to sender the signal
from django.contrib.auth.models import User

#reciever of the signal
from django.dispatch import receiver

from .models import Profile

@receiver(post_save,sender=User)
def create_profile(sender,instance,created,**kwargs):

    '''
        post_save:is the signal that is fired after and object is saved

        User:model is the sender of the signal

        receiver:is the create profile function that fetches the signal and performs some task

        instance:is the instance of User class

        created : if user was created

        Profile.objects.create(user=instance):create a profile obj with the instance of the user that was created

    '''
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save,sender=User)
def save_profile(sender,instance,**kwargs):
    '''
    save profile once a user is saved
    '''
    instance.profile.save()
    