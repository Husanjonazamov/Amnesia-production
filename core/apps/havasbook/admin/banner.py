from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from modeltranslation.admin import TabbedTranslationAdmin
from django.utils.translation import gettext_lazy as _
from ..models import BannerModel


@admin.register(BannerModel)
class BannerAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = (
        "id",
        "image_preview",  
        "link",
        "created_at",
    )
    search_fields = ("link",)
    readonly_fields = ("created_at",)

    @admin.display(description=_("Rasm"))
    def image_preview(self, obj):
        """Banner rasmi uchun preview — inline CSS bilan."""
        if obj.image:
            return format_html(
                """
                <div style="
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    background: #f9f9f9;
                    border: 1px solid #e5e7eb;
                    border-radius: 12px;
                    width: 120px;
                    height: 80px;
                    overflow: hidden;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.12);
                ">
                    <img src="{}" style="
                        width: 100%;
                        height: 100%;
                        object-fit: cover;
                        border-radius: 12px;
                    " />
                </div>
                """,
                obj.image.url
            )
        return format_html('<span style="color:#999;">Rasm yo‘q</span>')
