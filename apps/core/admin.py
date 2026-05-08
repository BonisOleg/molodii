"""Core admin: SiteSettings singleton with Unfold theme."""
from __future__ import annotations

from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from .models import SiteSettings


class SingletonAdmin(ModelAdmin):
    """Unfold-based mixin: prevents create/delete, auto-redirects changelist to the single object."""

    def has_add_permission(self, request):
        return not self.model.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = self.model.objects.first()
        if obj is None:
            return HttpResponseRedirect(
                reverse(
                    f"admin:{self.model._meta.app_label}_{self.model._meta.model_name}_add"
                )
            )
        return HttpResponseRedirect(
            reverse(
                f"admin:{self.model._meta.app_label}_{self.model._meta.model_name}_change",
                args=[obj.pk],
            )
        )


@admin.register(SiteSettings)
class SiteSettingsAdmin(SingletonAdmin):
    compressed_fields = True

    readonly_fields = ("og_image_preview",)

    fieldsets = (
        (
            "Бренд",
            {
                "fields": ("brand_name_uk", "brand_name_it", "tagline_uk", "tagline_it"),
                "classes": ["tab"],
            },
        ),
        (
            "Контакт",
            {
                "fields": ("email", "phone"),
                "classes": ["tab"],
            },
        ),
        (
            "Соц. шеринг",
            {
                "fields": ("og_image", "og_image_preview"),
                "classes": ["tab"],
            },
        ),
    )

    @admin.display(description="Попередній перегляд OG-зображення")
    def og_image_preview(self, obj):
        if obj and obj.og_image:
            return format_html(
                '<img src="{}" style="max-height:120px;border-radius:6px;" />',
                obj.og_image.url,
            )
        return "—"
