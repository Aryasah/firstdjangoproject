from accounts.models import Profile
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
# Create your views here.



def login_attempt(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        

        # check if user has entered correct credentials
        user = authenticate(username=username, password=password)

        if user is not None:
            # A backend authenticated the credentials
            login(request, user)
            messages.success(request,"Succesful Logged-In")
            return redirect("/")

        else:
            # No backend authenticated the credentials
            messages.error(request,"Invalid Credentials ,Please Try Again")
            return render(request, 'accounts/login.html')

    return render(request, 'accounts/login.html')




def register_attempt(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(password)

        try:
            if User.objects.filter(username = username).first():
                messages.error(request, 'Username is taken.')
                return redirect('/register')

            if User.objects.filter(email = email).first():
                messages.error(request, 'Email is taken.')
                return redirect('/register')
            
            user_obj = User(username = username , email = email)
            user_obj.set_password(password)
            user_obj.save()
            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(user = user_obj , auth_token = auth_token)
            profile_obj.save()
            send_mail_after_registration(email , auth_token)
            return redirect('/token')

        except Exception as e:
            print(e)


    return render(request , 'accounts/register.html')

def success(request):
    return render(request , 'accounts/success.html')


def token_send(request):
    return render(request , 'accounts/token_send.html')



def verify(request , auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
    

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('/accounts/login')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('/accounts/login')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)
        return redirect('/')

def error_page(request):
    return  render(request , 'accounts/error.html')


# Create your views here.
def index(request):
    if request.user.is_anonymous:
        return redirect('/accounts/login') 
    return render(request, 'accounts/home.html')



def about(request):
    return render(request, 'accounts/about.html') 

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')
        contact = Contact(name=name, email=email, phone=phone, desc=desc, date = datetime.today())
        contact.save()
        messages.success(request, 'Your message has been sent!')
    return render(request, 'accounts/contact.html')

def logoutUser(request):
    logout(request)
    messages.success(request,"Succesful Logout")

    return redirect("/accounts/login")




def send_mail_after_registration(email , token):
    subject = 'Your accounts need to be verified'
    message = f'Hi paste the link to verify your account http://aryasah17.herokuapp.com/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )
    