from django.contrib import admin
from users.models import User, Follow


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Admin class for custom user."""

    list_display = ['email', 'username', ]
    search_fields = ['email', 'username', ]


admin.site.register(Follow)
