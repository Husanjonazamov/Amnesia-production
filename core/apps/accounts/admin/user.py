from django.contrib.auth import admin
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm  # UserCreationForm,
from unfold.forms import UserChangeForm
from django.utils.html import format_html



class CustomUserAdmin(admin.UserAdmin, ModelAdmin):
    change_password_form = AdminPasswordChangeForm
    # add_form = UserCreationForm
    form = UserChangeForm
    list_display = (
        "id",
        "role_badge",
        "phone",
        "email",
        "user_id",
        "created_at",
        "is_active",
    )
    list_display_links = ("id", "role_badge")
    list_filter = ("role", "is_active",)
    search_fields = ("phone", "email", "username", "user_id")
    ordering = ("-created_at",)
    readonly_fields = ("last_login", "date_joined", "created_at")
    
    autocomplete_fields = ["groups", "user_permissions"]
    fieldsets = ((None, {"fields": ("phone", "user_id")}),) + (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                    "role",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    
    # @admin.display(description="Role", ordering="role")
    def role_badge(self, obj):
        """Rangli badge ko‘rinishida role ni qaytaradi."""
        role = getattr(obj, "role", "user") or "user"

        # Ranglar va nomlar mapping
        mapping = {
            "superuser": ("Superuser", "#e11d48", "#fff"),
            "admin": ("Admin", "#4f46e5", "#fff"),
            "user": ("User", "#059669", "#fff"),
        }
        label, bg, color = mapping.get(role, ("User", "#0891b2", "#fff"))

        # Inline CSS bilan chiroyli badge yaratamiz
        return format_html(
            """
            <span style="
                background: {bg};
                color: {color};
                padding: 4px 10px;
                border-radius: 12px;
                font-size: 12px;
                font-weight: 600;
                text-transform: capitalize;
                box-shadow: 0 1px 3px rgba(0,0,0,0.2);
                ">
                {label}
            </span>
            """,
            bg=bg,
            color=color,
            label=label,
        )


class PermissionAdmin(ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


class GroupAdmin(ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
    autocomplete_fields = ("permissions",)


class SmsConfirmAdmin(ModelAdmin):
    list_display = ["phone", "code", "resend_count", "try_count"]
    search_fields = ["phone", "code"]
