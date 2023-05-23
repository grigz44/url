from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import URLMapping

import pyshorteners



from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        # Check if passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')
        
        # Create the user
        user = User.objects.create_user(username=username, password=password)
        user.save()
        
        messages.success(request, 'Registration successful. You can now log in.')
        return redirect('login')
    
    return render(request, 'register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('shorten_url')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('register')
    
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    messages.success(request, 'Logout successful.')
    return redirect('login')

from django.contrib.auth.decorators import login_required
from pyshorteners.exceptions import ShorteningErrorException

@login_required(login_url='login')



def shorten_url(request):
    if request.method == 'POST':
        original_url = request.POST.get('original_url')
        type_bitly = pyshorteners.Shortener(api_key='034d67ad83e5498696b59d32cdeaef906abdc39d')

        try:
            short_url = type_bitly.bitly.short(original_url)
        except ShorteningErrorException:
            # Handle the exception when the URL shortening fails
            error_message = "Invalid URL or error occurred during shortening."
            return render(request, 'shorten_url.html', {'error_message': error_message})

        # Check if the short URL already exists in the database
        if URLMapping.objects.filter(shortened_url=short_url, user=request.user).exists():
            # Handle the case of a duplicate entry
            return render(request, 'shorten_url.html', {'short_url': short_url})
        else:
            # Save the URLMapping object if it's not a duplicate
            url_mapping = URLMapping(original_url=original_url, shortened_url=short_url, user=request.user)
            url_mapping.save()

            return render(request, 'shorten_url.html', {'short_url': short_url})

    return render(request, 'shorten_url.html', {})


