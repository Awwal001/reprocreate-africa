from django.contrib import admin
from .models import User, UserProfile, Address, Avatar, Permission, UserPermission


class UserAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'auth_provider', 'created_at']


admin.site.register(User, UserAdmin)
admin.site.register(UserProfile)
admin.site.register(Address)
admin.site.register(Avatar)
admin.site.register(Permission)
admin.site.register(UserPermission)