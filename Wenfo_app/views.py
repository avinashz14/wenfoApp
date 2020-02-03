from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from .models import User


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
		user = authenticate(username = username, password = password)
		if user:
			login(request,user)
		return HttpResponseRedirect(reverse('dashboard'))

	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			return HttpResponseRedirect(reverse('dashboard'))

		return render(request,'signin.html')


class DashboardView(TemplateView):
	template_name = "dashboard.html"

class CreateprofileView(TemplateView):
	template_name = 'createprofile.html'
	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super().get_context_data(**kwargs)
		# Add in a QuerySet of all the books
		context['user'] = self.request.user
		return context

	def post(self, request, *args, **kwargs):
		context = super(CreateprofileView, self).get_context_data(*args, **kwargs)
		user= request.user

		if 'username' in request.POST:
			username = request.POST.get('username')
			update_user = User.objects.get(username=user.username)
			update_user.username = username
			update_user.save()

		if 'phone' in request.POST:
			phone = request.POST.get('phone')
			user.phone = phone
			user.save()

		if 'url_link' in request.POST:
			url_link = request.POST.get('url_link')
			user = User.objects.get(username=user.username)
			user.url_link = url_link
			user.save()

		if 'password' in request.POST:
			password= request.POST.get('password')
			confirm_password= request.POST.get('confirm_password')
			context["page"] = "change_password"
			context["status"] = "PasswordNotMatched"
			if password == confirm_password:
					user = request.user
					user.set_password(password)
					user.save()
					context["status"] = "Success"
		return super(TemplateView, self).render_to_response(context)


