import json 
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.contrib import messages

# Create your views here.
def register(request):
    if request.method=='GET':
        return render(request,'auth/register.html')
    if request.method=='POST':
        data = json.loads(request.body)
        username = data['username']
        email = data['email']
        password = data['password']
        user = User.objects.create(username=username,email=email,password=password)
        user.save()
        return redirect('auth/login.html')

def login_user(request):
    if request.method == 'GET':
        return render(request, 'auth/login.html')        
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        context = {'username': username,
                   'password':password}
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # Redirect to the home page after successful login
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, 'auth/login.html',context )
    

def validate_username(request):
    if request.method =='POST':
        data = json.loads(request.body)
        username = data['username']
        if username[0].isdigit():
            return JsonResponse({'username_error':'username should start with a letter'})
        if User.objects.filter(username = username):
            return JsonResponse({'username_error':'username is already taken'})
        return JsonResponse({'valid':True})
    
def validate_mail(request):
    if request.method =='POST':
        data = json.loads(request.body)
        email = data['email']
        if email:
           try:
                validate_email(email)
           except ValidationError:
                return JsonResponse({'email_error': 'Invalid Email'})
        if User.objects.filter(email = email):
            return JsonResponse({'email_error':'email is already taken'})
        return JsonResponse({'valid':True})

def validate_pass(request):
    if request.method =='POST':
        data = json.loads(request.body)
        password = data['password']
        if password:
           try:
                validate_password(password)
           except ValidationError:
                return JsonResponse({'pass_error': 'Please Write a Strong Password'})
        return JsonResponse({'valid':True})

def check_password_match(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        password = data['password']
        re_password = data['re_password']
        
        if password != re_password:
            return JsonResponse({'password_error': 'Passwords do not match'})
        
        return JsonResponse({'valid': True})