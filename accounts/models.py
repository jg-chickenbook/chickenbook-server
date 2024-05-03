from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator


phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                             message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    is_visible = models.BooleanField(default=True)
    status = models.CharField(("Status"), max_length=20, blank=True) 
    name = models.CharField(("Full name"), max_length=50, blank=True) 
    headline = models.CharField(("Headline"), max_length=20, blank=True) 
    mainSkills = models.CharField(("Main Skills"), max_length=50, blank=True) 
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)  # Adjust the max_length accordingly
    email = models.EmailField(("Email"), max_length=30, blank=True) 
    about = models.CharField(("About..."), max_length=1000, blank=True) 




    def __str__(self):
        return self.user.username
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()