from django.contrib import admin
from django.contrib.auth import get_user_model

user = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ['email', 'first_name', 'last_name']
    # TODO
    list_filter = ('role', )


admin.site.register(user, UserAdmin)
