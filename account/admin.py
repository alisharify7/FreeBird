from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import User, Object


UserAdmin.fieldsets[1][1]['fields'] += ("phone",)
admin.site.register(User, UserAdmin)

admin.site.register(Object)