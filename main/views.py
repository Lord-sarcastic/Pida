from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from django.db.models import Q, F, Count
from .models import Key
from .forms import *

class SignUpView(View):
    template_name = 'main/signup.html'
    
    def get_queryset(self):
        return User.objects.all()
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        form = CreateUserForm(request.POST)
#        if form.is_valid():
        if form['password'].data != form['confirm_password'].data:
            return render(request, self.template_name, {'warning' : 'Passwords do not match.'})

        if len(form['password'].data) < 8:
            return render(request, self.template_name, {'warning' : 'Password too short, should not be less than 8 characters.'})

        try:
            user = User.objects.get(username=form['username'].data.lower())
            return render(request, self.template_name, {'warning' : 'Username already exists.'})
        except User.DoesNotExist:
            user = User.objects.create_user(form['username'].data.lower(), email=form['email'].data, password=form['password'].data, first_name=form['first_name'].data.capitalize(), last_name=form['last_name'].data.lower())
        user = authenticate(username=user.username, password=form['password'].data)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/secure-digit/')
        else:
            return HttpResponse("<h1>This user is not yet authenticated, contact the admin for more information or create a new account</h1>")
#        else:
#            return render(request, self.template_name, {'warning' : f"Form not valid!{form['username'].data.lower()}: {form['email'].data} : {form['password'].data}: {form['first_name'].data} : {form['last_name'].data}: {form['confirm_password'].data}"})
    
    
class SignInView(View):
    template_name = 'main/signin.html'
    
    def get_queryset(self):
        return User.objects.all()
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        form = UserLoginForm(request.POST)
#        if form.is_valid():
        try:
            user = User.objects.get(username=form['username'].data.lower())
            if user.check_password(form['password'].data):
                user = authenticate(username=user.username, password=form['password'].data)
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect('/secure-digit/')
                else:
                    return HttpResponse("<h1>This user is not yet authenticated, contact the admin for more information or create a new account</h1>")
            else:
                return render(request, self.template_name, {'warning' : 'Wrong password!'})
        except User.DoesNotExist:
            return render(request, self.template_name, {'warning' : 'User does not exist.'})
#        else:
#            return render(request, self.template_name, {'warning' : f"Form not valid!"})
            
        
class MainView(LoginRequiredMixin, View):
    login_url = '/'
    template_name = 'main/main.html'
    
    def get_queryset(self):
        return User.objects.all()
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        form = SecureKeyForm(request.POST)
#        if form.is_valid():
        if request.user.check_password(form['password'].data):
            if form['digit'].data == form['confirm_digit'].data:
                if form['end'].data < form['start'].data:
                    return render(request, self.template_name, {'warning' : 'Start value should be less than end value!'})
                key = Key(user=request.user, digit=form['digit'].data, start=form['start'].data, end=form['end'].data)
                key.save()
                return render(request, 'success.html')
            else:
                return render(request, self.template_name, {'warning' : 'Digits do not match!'})
        else:
            return render(request, self.template_name, {'warning' : 'Wrong password!'})
#        else:
#            return render(request, self.template_name, {'warning' : f"Form not valid!{form['username'].data.lower()}: {form['email'].data} : {form['password'].data}: {form['first_name'].data} : {form['last_name'].data}: {form['confirm_password'].data}"})