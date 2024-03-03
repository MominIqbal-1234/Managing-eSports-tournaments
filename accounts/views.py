from django.shortcuts import render,redirect
from django.contrib.auth.models import User
import requests
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login,logout
from django.views import View
from accounts.models import UserInfoURL
import hashlib
import random
import string
from django.conf import settings
from accounts.handle_mail import HandleMail
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib import messages


class HashAndGeneratePassword:
    def generate_password(length=12):
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(length))
        return password
    def hash_string(userpass):
        h = hashlib.new("SHA256")
        h.update(userpass.encode())
        return h.hexdigest()



GOOGLE_CLIENT_ID = '783594166641-0feidvckks3rttp2gmah654ctcotfg7d.apps.googleusercontent.com'
# GOOGLE_CLIENT_ID = '783594166641-0feidvckks3rttp2gmah654ctcotfg7d.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = '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'
# GOOGLE_CLIENT_SECRET = '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'
# REDIRECT_URI = 'http://mefiz.com/accounts/google-callback/'
REDIRECT_URI = 'http://127.0.0.1:8000/accounts/google-callback/'

def google_login(request):
    # Redirect the user to Google's OAuth2 authentication URL
    auth_url = f'https://accounts.google.com/o/oauth2/auth?client_id={GOOGLE_CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=email profile'
    return HttpResponseRedirect(auth_url)

def google_callback(request):
    # Handle the redirect from Google and exchange the authorization code for tokens
    code = request.GET.get('code')
    token_url = 'https://accounts.google.com/o/oauth2/token'
    payload = {
        'code': code,
        'client_id': GOOGLE_CLIENT_ID,
        'client_secret': GOOGLE_CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code'
    }
    response = requests.post(token_url, data=payload)
    data = response.json()
    
    access_token = data.get('access_token')
    
    # Now, you have the access_token, use it to get user information from Google APIs
    user_info_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(user_info_url, headers=headers)
    user_info = response.json()
    id = (user_info['id'])
    email = (user_info['email'])
    name = (user_info['name'])
    picture = (user_info['picture'])
    username,domain = email.split("@")
    password = HashAndGeneratePassword.generate_password()
    hash_password = HashAndGeneratePassword.hash_string(password)
    try:
        if User.objects.filter(email=email).exists():
            userInfo = UserInfoURL.objects.get(id_user=id)
            user = authenticate(request, username=username, password=userInfo.user_auth)
            if user is not None:
                login(request, user)
        else:

            user = User.objects.create_user(
                    username=username,
                    email=email,
                    first_name=name,
                    password=hash_password
                        )
        
            UserInfoURL(id_user=id,picture_url=picture,user_auth=hash_password,user_id=user.id).save()
            user.save()
        user = authenticate(request, username=username, password=hash_password)
        if user is not None:
            login(request, user)
        return redirect('/')
    except Exception as e:
        return HttpResponse(e)

        






class HandleLogin(View):
    def get(self,request):
        if request.user.is_authenticated: 
            return redirect('/')
        return render(request,'login.html')
    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        messages.error(request, 'Wrong Username and Password')
        return redirect("/accounts/login/")
    


class CreateAccount(View):
    def get(self,request):
        print("signup")
        if request.user.is_authenticated:
            return redirect('/')
        return render(request,'signup.html')
    def post(self,request):
        if request.session["otp"] == int(request.POST.get('otp')):
            full_name = request.session["full_name"]
            email = request.session["email"]
            password = request.session["password"]
            username = request.session["username"] 
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=full_name,
                password=password
            ).save()
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
        else:
            messages.error(request, 'Wrong OTP')
            return render(request,'email_verify.html')


@method_decorator(csrf_exempt, name='dispatch')
class HandleSignup(View):
    def get(self,request):
        if request.user.is_authenticated:
            return redirect('/')
        return render(request,'signup.html')
    def post(self,request):
        HandleMail.sendVerifyMail(request)
        return render(request,'email_verify.html')




class HandleLogout(View):
    def get(self,request):
        logout(request)
        return redirect("/")
        

