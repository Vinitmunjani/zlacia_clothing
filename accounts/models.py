
from django.db import models
from base.models import BaseModel
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from base.emails import send_account_activation_email

class UserProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.IntegerField(default=0)
    gender = models.CharField(max_length=100,blank=True,null=True)
    is_email_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100,null=True,blank=True)



class UserAdd(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100,blank=True,null=True)
    addressline1  = models.CharField(max_length=100,default=None)
    addressline2  = models.CharField(max_length=100,default=None)
    pincode = models.IntegerField(default=0)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    class Meta:
        unique_together = ['user', 'addressline1','addressline2', 'pincode', 'city', 'state']


    # You can add more fields to store additional user information
