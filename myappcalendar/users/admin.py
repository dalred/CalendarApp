from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db.models import Count
user = get_user_model()


class UserAdmin(admin.ModelAdmin):
    readonly_fields = ("last_login",)
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ['email', 'first_name', 'last_name']
    # TODO
    list_filter = ('role',)

    #list_filter = ('is_staff', )



admin.site.register(user, UserAdmin)
