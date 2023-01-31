from django.contrib import admin
from .models import User, Questions, Mark, School, SchoolScore, Notification

# Register your models here.

admin.site.register(User)
admin.site.register(Questions)
admin.site.register(Mark)
admin.site.register(School)
admin.site.register(SchoolScore)
admin.site.register(Notification)