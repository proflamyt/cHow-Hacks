from django.contrib import admin
from .models import  Questions, Mark, School, SchoolScore, Notification, User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _



# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = User

    # Display additional fields in user change form
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('username', 'first_name', 'last_name')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important datess'), {'fields': ('last_login', 'date_joined')}),
        # Add your custom fields here
        (_('Custom fields'), {'fields': ('changed_password', 'name' )}),
    )

    # Define the fields for the user creation form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'changed_password', 'name'),
        }),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Questions)
admin.site.register(Mark)
admin.site.register(School)
admin.site.register(SchoolScore)
admin.site.register(Notification)
