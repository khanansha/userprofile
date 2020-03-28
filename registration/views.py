from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserSignUpForm, userform
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from .models import Registrations, OtpVerification
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django import forms
from django import forms
from django.core.validators import validate_email
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils.crypto import get_random_string


def usersignup(request):
    if request.method == "POST":
        username = request.POST.get('username', '')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        phone_no = request.POST.get('phone_no', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        #un= Registrations.objects.filter( username= username)
        # un=Registrations.objects.filter(username=username)
        #email = Registrations.objects.filter(email=email)
        # if email:
        # return HttpResponse("email is already exist")
      #  if un:
        # messages.error(request, 'username already exist')
        #template = "registration/signup.html"
        # return render(request, template)
        # return redirect(usersignup)

       # if confirm_password != password:
        #  messages.error(request, 'confirm password does not matched with password')
        #template = "registration/signup.html"
        # return render(request, template)
        #  return redirect(usersignup)

        registers = Registrations(username=username, first_name=first_name, last_name=last_name,
                                  phone_no=phone_no, email=email, password=password, confirm_password=confirm_password)
        registers.save()

        ######################### mail system ####################################
        # current_site = get_current_site(request)
        # email_subject = 'Activate Your Acount'
        # message = render_to_string('registration/acc_active_email.html', {
        #     'user': registers,
        #     'domain': current_site.domain,
        #     'uid': urlsafe_base64_encode(force_bytes(registers.pk)).decode(),
        #     #'uid': registers.pk,
        #     'token': account_activation_token.make_token(registers),
        #     #'token': '6789',
        #     })
        # to_email = request.POST.get('email', '')
        # email = EmailMessage(email_subject, message, to=[to_email])
        # email.send()

        current_site = get_current_site(request)
        # to_email = request.POST.get('email', '')
        # email_subject = 'Activate Your Acount'
        # message = 'Please activate your account <a href="'+ current_site.domain +'/activate?email='+to_email+'" target="_blank">Click here</a>'
        # send_mail(email_subject, message, 'anjumkhan88987@gmail.com', [to_email], fail_silently=False,)
        subject, from_email, to = 'Activate Your Acount', 'anjumkhan88987@gmail.com', request.POST.get(
            'email', '')
        text_content = ''
        html_content = 'Please activate your account <a href="http://' + \
            current_site.domain + '/activate_email?e='+to+'" target="_blank">Click here</a>'
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return HttpResponse('We have sent you an email, please confirm your email address to complete registration')
    else:
        return render(request, 'registration/signup.html')


def activate(request):
    e = request.GET.get('e', '')
   # u = request.GET.get('username', '')
    # u=Registrations.objects.all()
    Registrations.objects.filter(email=e).update(is_active="1")
    # select name from registration where email=e
    u = Registrations.objects.filter(email=e)
    return HttpResponse("Thanks " + u[0].first_name + " " + u[0].last_name + " for your email varification")


def signup(request):
    if request.method == 'POST':
        form = userform(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_no = form.cleaned_data['phone_no']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            # return HttpResponse(phone_no)
            registers = Registrations(username=username, first_name=first_name, last_name=last_name,
                                      email=email, phone_no=phone_no, password=password, confirm_password=confirm_password)
            registers.save()
            current_site = get_current_site(request)
            subject, from_email, to = 'Activate Your Acount', 'anjumkhan88987@gmail.com', email
            text_content = ''
            html_content = 'Please activate your account <a href="http://' + \
                current_site.domain + '/activate_email?e='+to+'" target="_blank">Click here</a>'
            msg = EmailMultiAlternatives(
                subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return HttpResponseRedirect('/signup/?message=We have sent you an email, please confirm your email address to complete registration')
    else:
        form = userform()

    msg = request.GET.get('message', '')
    return render(request, 'registration/signupp.html', {'form': form, 'msg': msg})


def otpsignup(request):
    if request.method == 'POST':
        form = userform(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_no = form.cleaned_data['phone_no']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            #OTP= form.cleaned_data['OTP']
            registers = Registrations(username=username, first_name=first_name, last_name=last_name,
                                      email=email, phone_no=phone_no, password=password, confirm_password=confirm_password)
            registers.save()

            u = Registrations.objects.filter(email=email)
            uid = u[0].id

            randotp = get_random_string(6, allowed_chars='0123456789')
            # return HttpResponse(randotp)
            otpver = OtpVerification(
                OTP=randotp, registration_id=uid, phone_no=phone_no)
            otpver.save()

            current_site = get_current_site(request)
            subject, from_email, to = 'Activate Your Acount', 'anjumkhan88987@gmail.com', email
            text_content = ''
            # html_content = 'Please activate your account <a href="http://' + \
            # current_site.domain + '/activate_email?e='+to+'" target="_blank">Click here</a>'
            html_content = 'Hii'+first_name + ' ' + last_name + 'your OTP is ' + randotp
            msg = EmailMultiAlternatives(
                subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return HttpResponseRedirect('/otpform/?regid='+str(uid))
    else:
        form = userform()
    return render(request, 'registration/otpreg.html', {'form': form})


def otpform(request):
    if request.method == "POST":
        OTP = request.POST.get('OTP', '')
        var_reg_id = request.POST.get('reg_hidden_id', '')

        #randotp= request.GET.get('randotp', '')
        # select * from otp_table WHERE otp = OTP
        # o/p:select * from otp_table WHERE otp = 4567
        # select * from otp_table WHERE otp = OTP AND reg_id = var_reg_id
        # o/p: select * from otp_table WHERE otp = 4567 AND reg_id = 95
        u = OtpVerification.objects.filter(OTP=OTP, registration_id=var_reg_id)
        # regid = OtpVerification.objects.filter(registration_id= var_reg_id)
        #uotp = u[0].OTP
        # return HttpResponse(u)
        if u:
            # update is_active column in registration table
            Registrations.objects.filter(id=var_reg_id).update(is_active="1")
            return HttpResponse("Thank you so much")
        else:
            messages.error(request, "invalid OTP")
            return HttpResponseRedirect('/otpform/?regid='+var_reg_id)
            # return HttpResponse("Thank you so much")

    else:

        regid = request.GET.get('regid', '')
        # return HttpResponse(regid)
        return render(request, 'registration/otp.html', {'regid': regid})
