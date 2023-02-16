from django.contrib import admin
from .models import  Questions, Mark, School, SchoolScore, Notification
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(Questions)
admin.site.register(Mark)
admin.site.register(School)
admin.site.register(SchoolScore)
admin.site.register(Notification)
