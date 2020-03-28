from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
#from .models import *
from .models import Registrations ,OtpVerification
class UserSignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=100, help_text='Required')
    phone_no = forms.CharField(max_length = 20)
    class Meta:  
        model = User  
        fields = ('email', 'first_name', 'last_name', 'username','phone_no','password',)


class userform(forms.ModelForm):
    username=forms.CharField(widget=forms.TextInput, required=True,max_length=50)
    first_name=forms.CharField(widget=forms.TextInput, required=True,max_length=50) 
    last_name=forms.CharField(widget=forms.TextInput, required=True,max_length=50)      
    email=forms.CharField(widget=forms.EmailInput, required=True,max_length=50)
    phone_no=forms.CharField(widget=forms.TextInput, required=True,max_length=50)
    password=forms.CharField(widget=forms.TextInput, required=True,max_length=50)
    confirm_password=forms.CharField(widget=forms.TextInput,max_length=50)
    #registration=forms.ModelChoiceField(queryset=OtpVerification.objects.all())
    #OTP=forms.CharField(widget=forms.TextInput,max_length=10)
    class Meta:  
        model = Registrations  
        fields = ('email', 'first_name', 'last_name', 'username','phone_no','password','confirm_password')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        username_qs = Registrations.objects.filter(username=username)
        if username_qs.exists():
            raise forms.ValidationError("This username already exists.")
        return username 

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_qs = Registrations.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("This email already exists.")
        return email  
    def clean_confirm_password(self):
        password=self.cleaned_data['password']
        confirm_password=self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError("password and confirm_password does not match")
        return password





