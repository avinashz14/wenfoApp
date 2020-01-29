from django.shortcuts import render

# some_app/views.py
from django.views.generic import TemplateView


class SignupView(TemplateView):
    template_name = "signup.html"

class SigninView(TemplateView):
    template_name = "signin.html"

class DashboardView(TemplateView):
    template_name = "dashboard.html"

class CreateprofileView(TemplateView):
    template_name = "Createprofile.html"
