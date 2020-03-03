from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import News, UrlLink, PhoneNumber
from .models import News,Notification
User = get_user_model()


admin.site.register(User)
admin.site.register(News)
admin.site.register(UrlLink)
admin.site.register(PhoneNumber)
admin.site.register(Notification)
