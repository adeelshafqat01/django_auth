from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# from .forms import AddressForm
from .models import *

"""class AddressAdmin(admin.ModelAdmin):
    form = AddressForm
    model = Address"""


class CustomUserAdmin(UserAdmin):
    list_display = ["id", "email", "password"]
    list_filter = ["email"]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "is_active",
                    "last_login",
                    "is_superuser",
                    "date_joined",
                    "first_name",
                    "last_name",
                    "is_staff",
                    "is_verified",
                )
            },
        ),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (
            None,
            {"classes": ("wide",), "fields": ("email", "password")},
        ),
    )
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = ()


admin.site.register(User, CustomUserAdmin)
# admin.site.register(Address, AddressAdmin)
