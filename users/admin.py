from django.contrib import admin

from users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'last_activity',)
    ordering = ('email', 'first_name', 'last_name', 'last_activity',)


admin.site.register(User, UserAdmin)
