from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm = request.POST['confirm_password']

        if password != confirm:
            messages.error(request, "Passwords don't match")
            return redirect('register')

        if User.objects.filter(username = username).exists():
            messages.error(request, "This Username already exists!")
            return redirect('register')
        
        user = User.objects.create_user(username = username, password = password, email = email)
        messages.success(request, "Account created succesfully!")
        return redirect('login')

    return render(request, 'register.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
 
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
 
        user = authenticate(request, username=username, password=password)
 
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Username or Password incorrects.')
            return redirect('login')
 
    return render(request, 'login.html')
 
 
def logout_view(request):
    logout(request)
    return redirect('login')

def forgot_password_view(request):
    return render(request, 'forgot.html')