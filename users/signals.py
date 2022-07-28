from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

from django.conf import settings
from django.core.mail import send_mail


#@receiver(post_save,sender=Profile)
def CreateProfile(sender,instance,created, **kwargs):
    print('Profile signal triggered')
    if created:
        user=instance
        profile=Profile.objects.create(
            user=user,
            user_name=user.username,
            email=user.email,
            name=user.first_name,
        )    

        subject='Welcome to Devsearch!'
        body='We are glad you are here.'
        send_mail(
            subject,
            body,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False,
        )

def UpdateUser(sender,instance,created,**kwargs):
    profile=instance
    user=profile.user
    if created ==False:
        user.first_name=profile.name
        user.username=profile.user_name
        user.email=profile.email
        user.save()

def DeleteUser(sender,instance,**kwargs):
    try:
        user=instance.user
        user.delete()
    except:
        pass

post_save.connect(CreateProfile,sender=User)
post_save.connect(UpdateUser,sender=Profile)
post_delete.connect(DeleteUser,sender=Profile)