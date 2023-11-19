from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

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
        elif password != confirmpassword:
            messages.error(request, message='Password does not match',extra_tags='danger')
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
        if not user.exists():
            messages.error(request, message= 'Invalid Username', extra_tags='danger')
            return redirect('/login')
        
        user = authenticate(username = username, password = password)
        if user is None:
            messages.error(request, message='Invalid Password')
            return redirect('/login')
        else:
            login(request,user)
            messages.success(request, message='Login Successfull')
            return redirect('/home')

    return render(request, 'login.html',context={'title':'Login'})

def logout_view(request):
    logout(request)
    messages.success(request, message='Logout Successfull')
    return redirect('/login')


@login_required(login_url='/login')
def home(request):
    return render(request, 'home.html')