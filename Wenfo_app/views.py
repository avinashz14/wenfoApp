
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.contrib.auth import logout
import random

from .models import User,News,Notification,PhoneNumber,UrlLink




class SignupView(TemplateView):
	def post(self, request, *args, **kwargs):
		username = request.POST.get('username')
		email= request.POST.get('email')
		phone= request.POST.get('phone')
		password= request.POST.get('password')
		confirm_password= request.POST.get('confirm_password')
		
		if password==confirm_password:
			user = User(username=username,email=email,password=password)
			user.set_password(password)
			user.save()
			number = PhoneNumber.objects.create(phone_number=phone, user=user)
			return HttpResponseRedirect(reverse('signin'))
		
	
	def get(self, request, *args, **kwargs):			
		return render(request,'signup.html')

 
class SigninView(TemplateView):
	def post(self, request, *args, **kwargs):
		username = request.POST.get('username')
		password= request.POST.get('password')
		user = authenticate(username = username, password = password)
		if user:
			login(request,user)
			return HttpResponseRedirect(reverse('worldnews'))
		return render(request,'signin.html',{"message":"Invalid Username and Password"})

	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			return HttpResponseRedirect(reverse('worldnews'))

		return render(request,'signin.html')


class DashboardView(TemplateView):
	def get(self,request, *args, **kwargs):
		news=News.objects.filter(author=request.user)
		user = request.user
		phone_no = PhoneNumber.objects.filter(user=user)
		return render(request,'dashboard.html',{"news":news,"user":user,"number":phone_no})

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

class AllNewsView(TemplateView):
	def get(self,request, *args, **kwargs):
		news=News.objects.order_by('date')
		user = request.user
		user_data = User.objects.get(username=user.username)
		print(news.values())
		return render(request,'worldnews.html',{"news":news,"user":user_data})

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

class NotificationView(TemplateView):
	def get(self,request, *args, **kwargs):
		notification=Notification.objects.all()
		print(notification.values())
		return render(request,'notifications.html',{"notification":notification})

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

class RecommendationView(TemplateView):
	@method_decorator(login_required)
	def get(self,request, *args, **kwargs):
		return render(request,'recommendation.html')

		

class EditProfileView(TemplateView):
	template_name = 'createprofile.html'

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super().get_context_data(**kwargs)
		# Add in a QuerySet of all the books
		context['user'] = self.request.user
		return context

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def get(self,request, *args, **kwargs):
		user = request.user
		phone_no = PhoneNumber.objects.filter(user=user)
		phone_no = phone_no[0].phone_number
		availabe_username = [user.username+"_"+str(random.randint(0, 100)),user.email[:5]+"_"+user.username,user.username+"3214",user.username+phone_no[:4]]
		
		user_names=[]
		for name in User.objects.all():
			user_names.append(name.username)
		for name in availabe_username:
			if name in user_names:
				availabe_username.remove(name)
		# random.randint(0, 5)
		context ={"number":phone_no,"user":user,"user_names":availabe_username}
		return render(request,'createprofile.html',context)
		

	def post(self, request, *args, **kwargs):
		context = super(EditProfileView, self).get_context_data(*args, **kwargs)
		user= request.user		
		update_user = User.objects.get(username=user.username)

		phone_no = PhoneNumber.objects.filter(user=user)
		phone_no = phone_no[0].phone_number
		availabe_username = [user.username+"_"+str(random.randint(0, 100)),user.email[:5]+"_"+user.username,user.username+"3214",user.username+phone_no[:4]]
		user_names=[]
		for name in User.objects.all():
			user_names.append(name.username)
		for name in availabe_username:
			if name in user_names:
				availabe_username.remove(name)			
		context["user_names"] = availabe_username
		context["user"] = user
		
		if 'username' in request.POST:
			username = request.POST.get('username')
			update_user = User.objects.get(username=user.username)

			context["page"] =  "change_username"
			context["status"] =  "not_change_username"

			if not username  in user_names:
				update_user.username = username
				update_user.save()
				context["status"] =  "change_username"
		
		if 'Phone' in request.POST:
			phone = request.POST.getlist('Phone')
			for i in phone:
				PhoneNumber.objects.create(phone_number=i, user=user)
			context["status"] =  "change_phone"
			context["page"] =  "change_phone"
			

		if 'Email' in request.POST:
			email = request.POST.get('Email')
			update_user.email = email
			update_user.save()
			context["status"] =  "change_email"
			context["page"] =  "change_email"
						

		if 'Url' in request.POST:
			url_link = request.POST.getlist('Url')
			for i in url_link:
				UrlLink.objects.create(url=i, user=user)
			context["status"] =  "change_urllink"
			context["page"] =  "change_urllink"
			

		if 'password' in request.POST:
			password= request.POST.get('password')
			confirm_password= request.POST.get('confirm_password')
			context["page"] =  "change_password"
			context["status"] = "PasswordNotMatched"
			if password == confirm_password:
				user = request.user
				user.set_password(password)
				user.save()
				context["status"] = "Success"
				return HttpResponseRedirect(reverse('signin'))
		
		return super(TemplateView, self).render_to_response(context)


class AddNews(TemplateView):
	def post(self, request, *args, **kwargs):
		print(request.POST)
		title = request.POST.get('title')
		body= request.POST.get('body')
		if 'myfile' in request.FILES:
			image= request.FILES['myfile']
		else:
			image = None
		news = News.objects.create(title=title,body=body,image=image,author=request.user)
		news.save()
		return HttpResponseRedirect(reverse('dashboard'))

	def get(self, request, *args, **kwargs):
		return HttpResponseRedirect(reverse('dashboard'))




def logout_view(request):
    logout(request)
    
    return HttpResponseRedirect(reverse('signin'))

