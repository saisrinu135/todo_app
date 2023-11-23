from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import tasks_model
from django.conf import settings
from django.core.mail import send_mail
import random
from uuid import uuid4
from django.http import HttpResponseRedirect

# Create your views here.

def register_view(request):
    if request.method=='POST':
        username = request.POST.get('username')
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')

        if User.objects.filter(username=username).exists():
            messages.error(request, message='Username Already Used', extra_tags='danger')
            return redirect('/register')
        
        elif User.objects.filter(email=email).exists():
            messages.error(request, message='Email already Used',extra_tags='danger')
            return redirect('/register')

        elif password != confirmpassword:
            messages.error(request, message='Password does not match',extra_tags='danger')
            return redirect('/register')
        
        else:
            user = User.objects.create (
                username = username,
                first_name = first_name,
                last_name = last_name,
                email = email
            )
            user.set_password(password)
            user.save()
            messages.success(request, message='You have registered successfully.')
            return redirect('/login')
    return render(request,'register.html',context = {'title':"Register"})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username = username)
        if user.exists():
            user = authenticate(username = username, password = password)
            if user is None:
                messages.error(request, message='Invalid Password',extra_tags='danger')
                return redirect('/login')
            else:
                login(request,user)
                messages.success(request, message='Login Successfull')
                return redirect('/home')
        else:
            messages.error(request, message= 'Invalid User', extra_tags='danger')
            return redirect('/login')

    return render(request, 'login.html',context={'title':'Login'})

def logout_view(request):
    logout(request)
    messages.success(request, message='Logout Successfull')
    return redirect('/login')


@login_required(login_url='/login')
def home(request):
    tasks = tasks_model.objects.filter(user = request.user)
    if request.method == 'POST':
        user = request.user
        task = request.POST.get('task')
        userdata = tasks_model.objects.create(user = user, task = task)
        userdata.save()
    return render(request, 'home.html',context={'title':'Todo - Home','tasks':tasks})

@login_required(login_url='/login')
def update_task(request, id):
    task = tasks_model.objects.get(id = id)
    task.completed = not task.completed
    task.save()
    return redirect('/home')

@login_required(login_url='/login')
def delete_task(request, id):
    task = tasks_model.objects.get(id = id)
    task.delete()
    return redirect('/home')

username = None
generated_otp = None
generated_token = None
def forget_password(request):
    if request.method == 'POST':
        if User.objects.filter(username = request.POST.get('username')).exists():
            global username
            username = request.POST.get('username')
            global generated_otp
            generated_otp = random.randint(1000,9999)
            user = User.objects.get(username = username)
            send_mail(
                subject='Password Reset',
                message=f'''Your One Time Password to reset the your password {generated_otp}. Don't share it with any one.''', from_email=settings.EMAIL_HOST_USER, recipient_list=[user.email]
                )
            global generated_token
            generated_token = uuid4()
            return redirect(f'/verify/{str(generated_token)}')
        else:
            messages.error(request, message='Invalid User')
            return redirect('/forgetpassword')
    return render(request,'forgetpassword.html',context={'title':'Forget Password'})


def verify(request, token):
    if str(generated_token) == token:
        if request.method == 'POST':
            user_otp = request.POST.get('otp')
            print(user_otp)
            if int(generated_otp) == int(user_otp):
                print(generated_otp)
                messages.info(request, message='OTP Sent to your registered mail')
                return redirect(f'/password-change/{generated_token}')
            else:
                messages.error(request, message='OTP did not match',extra_tags='danger')
                return HttpResponseRedirect(request.path_info)
        return render(request, 'verify.html',context={'title':'Verify OTP'})
    return redirect('/login')
        
def password_change(request, token):
    if token == str(generated_token):
        if request.method == 'POST':
            password = request.POST.get('password')
            confirmpassword = request.POST.get('confirmpassword')
            if password == confirmpassword:
                user = User.objects.get(username = username)
                user.set_password(password)
                user.save()
                messages.success(request, message='Password changed Successfully')
                return redirect('/login')
            else:
                messages.error(request, message='Password did not match',extra_tags='danger')
                return HttpResponseRedirect(request.path_info)
        return render(request, 'change_password.html', context={'title':'Change Password'})
    else:
        return redirect('/login')