from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserModel

from .forms import CustomUserCreationForm, CustomUserUpdateForm
from .models import CustomUser


class CustomUserModel(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserUpdateForm
    model = CustomUser
    list_display = ['email', 'username']


admin.site.register(CustomUser, CustomUserModel)
