from django.contrib import admin
from django.contrib.auth import get_user_model

user = get_user_model()
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name')
    search_fields = ['email', 'first_name', 'last_name']
    list_filter = ('is_staff',)

admin.site.register(user, UserAdmin)
