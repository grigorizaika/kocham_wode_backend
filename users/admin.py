from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    fields = ['email', 'name', 'surname',
              'preferences', 'is_staff', 
              'is_superuser',]
    fieldsets = []
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'name', 'surname', 'is_staff', 
                'is_superuser', 'password1', 'password2')
            }),
    )
    ordering = ('email',)
    list_display = ['email', 'name', 'surname']
    list_filter = ('is_staff',)
    readonly_fields = ('preferences',)
