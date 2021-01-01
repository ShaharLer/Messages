from django.contrib import admin
from .models import SystemUser, Message

admin.site.register(SystemUser)
admin.site.register(Message)
