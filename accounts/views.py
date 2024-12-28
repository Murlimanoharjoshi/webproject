from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .form import SignupForm, LoginForm
from .models import User

from django.core.mail import send_mail

def home(request):
    if request.method == 'POST':
        recipient = request.POST.get('recipient')
        message = request.POST.get('message')
        send_mail(
            'Message from Django App',
            message,
            'your_email@gmail.com',
            [recipient],
        )
        return render(request, 'home.html', {'success': 'Mail sent successfully!'})
    return render(request, 'home.html')



def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'accounts/success.html', {'message': 'Successfully Registered!'})
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form})  # This must match the template file

def login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user:
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'accounts/login.html', {'form': form, 'error': 'Invalid credentials'})
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})
