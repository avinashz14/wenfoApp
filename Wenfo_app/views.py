from django.shortcuts import render
from django.views.generic import TemplateView
from . models import User
from django.shortcuts import render
import request
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth import login,logout
from django.urls import reverse
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from . models import User

class SignupView(TemplateView):
	def post(self, request, *args, **kwargs):
		username = request.POST.get('username')
		email= request.POST.get('email')
		phone= request.POST.get('phone')
		password= request.POST.get('password')
		confirm_password= request.POST.get('confirm_password')
		user = User(username=username,email=email,mobile_number=phone,password=password,url_link="")
		if password==confirm_password:
			user.save()
			return HttpResponseRedirect(reverse('signin'))
	
	def get(self, request, *args, **kwargs):			
		return render(request,'signup.html')


class SigninView(TemplateView):
	def post(self, request, *args, **kwargs):
		username = request.POST.get('username')
		password= request.POST.get('password')
		user = User.objects.get(username=username) 
		login(request,user)
		return HttpResponseRedirect(reverse('dashboard'))

	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			return HttpResponseRedirect(reverse('dashboard'))
			
		return render(request,'signin.html')


class DashboardView(TemplateView):
    template_name = "dashboard.html"

class CreateprofileView(TemplateView):
	def post(self, request, *args, **kwargs):
		user= request.user

		if 'username' in request.POST:
			username = request.POST.get('username')
			update_user = User.objects.get(username=user.username)
			update_user.username = username
			update_user.save()

		if 'email' in request.POST:
			email = request.POST.get('email')
			update_user = User.objects.get(username=user.username)
			update_user.email = email
			update_user.save()

		if 'phone' in request.POST:
			phone = request.POST.get('phone')
			update_user = User.objects.get(username=user.username)
			update_user.phone = phone
			update_user.save()

		if 'url_link' in request.POST:
			url_link = request.POST.get('url_link')
			update_user = User.objects.get(username=user.username)
			update_user.url_link = url_link
			update_user.save()

		if 'password' in request.POST:
			password= request.POST.get('password')
			confirm_password= request.POST.get('confirm_password')
			if password == confirm_password:
				update_user = User.objects.get(username=user.username)
				update_user.password = password
				update_user.save()
		return HttpResponseRedirect(reverse('createprofile'))


	def get(self, request, *args, **kwargs):			
		return render(request,'createprofile.html')
