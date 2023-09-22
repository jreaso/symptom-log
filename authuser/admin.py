from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from authuser.models import Account

class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'role', 'date_joined', 'last_login', 'is_staff')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    readonly_fields = ('id', 'date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account, AccountAdmin)
