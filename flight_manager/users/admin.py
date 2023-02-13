from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

Users = get_user_model()


@admin.register(Users)
class UserAdmin(admin.ModelAdmin):

    list_display = ["username", "first_name", "is_superuser"]
    search_fields = ["first_name"]


admin.site.unregister(Group)
