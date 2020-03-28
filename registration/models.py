from django.db import models
from django.utils.html import mark_safe
from django.db import IntegrityError
Select_Location=(
 ('mumbai','Mumbai'),
 ('pune ', 'pune'),
 ('delhi','Delhi'),
 ('agra','Agra'),
 ('goa','Goa'),
)

Preferences=(
 ('Food & Dinings','Food & Dinings'),
 ('Travel & Outdoor ', 'Travel & Outdoor'),
 ('Events','Events'),
 ('Nightlife','Nightlife'),
 ('Gifts & Shopping','Gifts & Shopping'),
 ('Deals & Offers','Deals & Offers'),
)
# Create your models here.

class Registrations(models.Model):
    username=models.CharField(max_length=50 , default='',unique = True, 
                    error_messages ={ 
                    "unique":"user already exist."
                    } )
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    phone_no=models.CharField(max_length=50, default='')
    email=models.EmailField( default='',unique = True, 
                    error_messages ={ 
                    "unique":"This email Id already exist."
                    } )
    password=models.CharField(max_length=10)
    confirm_password=models.CharField(max_length=10)
    OTP=models.CharField(max_length=20,default='')
    is_active=models.IntegerField(default=0)
    def __str__(self):
        return self.username

class Profile(models.Model):
    user=models.ForeignKey(Registrations, on_delete=models.CASCADE, related_name='Registrations')
    #images_upload = models.ImageField(upload_to='dining/images',default="")

    DOB=models.DateField()
    Select_Preferred_Location=models.CharField(max_length=1000, choices=Select_Location)
    def __str__(self):
        return self.user.username

class Preferences(models.Model):
    user=models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='Profile')
    Preferences=models.CharField(max_length=1000, choices=Preferences)
    images = models.ImageField(upload_to='registrations/images',default="")

class OtpVerification(models.Model):
    registration=models.ForeignKey(Registrations, on_delete=models.CASCADE, related_name='register')
    OTP=models.CharField(max_length=20,default='')
    phone_no=models.CharField(max_length=50, default='')
    def __str__(self):
        return self.registration.username



