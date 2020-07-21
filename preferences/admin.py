from django.contrib import admin

from .models import Preferences

@admin.register(Preferences)
class PreferencesAdmin(admin.ModelAdmin):
    list_display=('pk', 'weight', 'cup_vol', 'height', 'is_male', 'user')