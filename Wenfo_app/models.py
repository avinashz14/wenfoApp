from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
	username = models.CharField(max_length=100, unique=True)
	email = models.CharField(max_length=100)	
	mobile_number = models.CharField(max_length=100)
	password = models.CharField(max_length=100)
	url_link = models.CharField(max_length=100,blank=True,null=True)
