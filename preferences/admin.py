from django.contrib import admin

from .models import Preferences

@admin.register(Preferences)
class PreferencesAdmin(admin.ModelAdmin):
    list_display=('pk', 'weight', 'cup_vol', 'get_user')

    def get_user(self, obj):
        return obj.get_user()

    get_user.short_description = 'These preferences\' owner'

    def has_delete_permission(self, request, obj=None):
        return False
