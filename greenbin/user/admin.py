from django.contrib import admin
from user.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
#To add a profile model’s fields to the user page in the admin, define an InlineModelAdmin

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Profiles"

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline]

admin.site.unregister(User)
admin.site.register(Profile)
admin.site.register(User, UserAdmin)