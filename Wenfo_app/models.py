from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
	mobile_number = models.CharField(blank=True,null=True,max_length=100)
	loct_of_interest = models.CharField(blank=True,null=True,max_length=100)
	reward_points = models.IntegerField(blank=True,null=True)
	url_link = models.CharField(max_length=100,blank=True,null=True)

class Category(models.Model):
	name = models.CharField(max_length=100, default="")

class Keyword(models.Model):
	name = models.CharField(max_length=100, unique=True)
	category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, blank=True, null=True)
	strength = models.FloatField(max_length=100, default=0)

class News(models.Model):
	title = models.CharField(max_length=100)
	slug = models.SlugField(max_length=100, blank=True, null=True)
	image = models.FileField(max_length=100, blank=True, null=True)
	body = models.TextField(max_length=100, blank=True, null=True)
	author = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
	keywords = models.ManyToManyField(Keyword, blank=True)

class Notification(models.Model):
	title = models.CharField(max_length=100, blank=True, null=True)
	by = models.CharField(max_length=100, blank=True, null=True)
	image = models.FileField(max_length=100, blank=True, null=True)
	shown = models.CharField(max_length=100, blank=True, null=True)

class WenfoTransaction(models.Model):
	timestamp = models.DateTimeField(max_length=100, unique=True)
	amount_debit = models.CharField(max_length=100, blank=True, null=True)
	image = models.FileField(max_length=100, blank=True, null=True)
	shown = models.BooleanField(max_length=100, default=False)

class Transaction(models.Model):
	timestamp = models.DateTimeField(max_length=100, unique=True)
	username = models.CharField(max_length=100, blank=True, null=True)
	adsSeen = models.BooleanField(max_length=100, default=False)
	adsPosted = models.BooleanField(max_length=100, default=False)
	newsPosted = models.BooleanField(max_length=100, default=False)
	newsRead = models.BooleanField(max_length=100, default=False)
