from django.shortcuts import render,redirect
from django.views import View
from django.http import JsonResponse
import json
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage

from django.contrib import auth
# Create your views here.

class userNameValidation(View):
    def post(self,request):
        data=json.loads(request.body)
        username=data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error':'username should only contaion characters'}, status=400)        
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error':'username already exists, try an uniques username '}, status=409)
        return JsonResponse({'username_valid':True})

class RegistrationView(View):
    def get(self,request):
        return render(request,'authentication/register.html')

    def post(self,request):
       
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']

        context={
            'fieldvalues': request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password)<6:
                    messages.error(request,'password must be greater than 6 characters')
                    return render(request,'authentication/register.html', context)
                user=User.objects.create_user(username=username,email=email)
                user.set_password(password)                       
                user.save()
                messages.success(request,'Account created successfully')
                
                
            return render(request,'authentication/register.html')
        return render(request,'authentication/register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if(user):
            print('true')
            auth.login(request, user)
            messages.success(request, 'logggedin successfully')
            return redirect('/')
        else:
            messages.error(request, 'Invalid Credentials')
            return render(request, 'authentication/login.html')
    else:
        return render(request, 'authentication/login.html')

class LogoutView(View):
    def post(self,request):
        auth.logout(request)
        messages.success(request,'You have been Logged out')
        return redirect('login')