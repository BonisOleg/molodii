"""Contacts admin: ContactsPage singleton, Offices, SocialLinks, ConsultationRequests."""
from __future__ import annotations

from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from apps.core.admin import SingletonAdmin

from .models import ConsultationRequest, ContactsPage, Office, SocialLink


@admin.register(ContactsPage)
class ContactsPageAdmin(SingletonAdmin):
    compressed_fields = True

    fieldsets = (
        (
            "Заголовок і вступ",
            {
                "fields": ("title_uk", "title_it", "intro_uk", "intro_it"),
                "classes": ["tab"],
            },
        ),
        (
            "Графік роботи",
            {
                "fields": ("working_hours_uk", "working_hours_it"),
                "classes": ["tab"],
            },
        ),
    )


@admin.register(Office)
class OfficeAdmin(ModelAdmin):
    compressed_fields = True
    list_display = ("city_uk", "address_uk", "order", "photo_preview")
    list_display_links = ("city_uk",)
    list_editable = ("order",)
    readonly_fields = ("photo_preview",)

    fieldsets = (
        (
            "Локація",
            {
                "fields": ("order", "city_uk", "city_it", "address_uk", "address_it", "map_url"),
                "classes": ["tab"],
            },
        ),
        (
            "Фото",
            {
                "fields": ("photo", "photo_preview"),
                "classes": ["tab"],
            },
        ),
    )

    @admin.display(description="Фото")
    def photo_preview(self, obj):
        if obj and obj.photo:
            return format_html(
                '<img src="{}" style="max-height:80px;border-radius:4px;" />',
                obj.photo.url,
            )
        return "—"


@admin.register(SocialLink)
class SocialLinkAdmin(ModelAdmin):
    list_display = ("platform_icon", "get_platform_display", "url", "order")
    list_display_links = ("get_platform_display",)
    list_editable = ("order",)
    list_per_page = 20

    fieldsets = (
        (
            None,
            {
                "fields": ("platform", "url", "order"),
            },
        ),
    )

    PLATFORM_ICONS = {
        "instagram": "📸",
        "linkedin": "💼",
        "facebook": "📘",
        "telegram": "✈️",
        "whatsapp": "💬",
        "email": "📧",
    }

    @admin.display(description="")
    def platform_icon(self, obj):
        icon = self.PLATFORM_ICONS.get(obj.platform, "🔗")
        return format_html('<span style="font-size:1.3rem;">{}</span>', icon)


@admin.register(ConsultationRequest)
class ConsultationRequestAdmin(ModelAdmin):
    list_display = ("name", "email", "status_badge", "created_at")
    list_display_links = ("name",)
    list_filter = ("status",)
    search_fields = ("name", "email", "message")
    readonly_fields = ("name", "email", "message", "created_at")
    list_per_page = 30
    date_hierarchy = "created_at"

    fieldsets = (
        (
            "Від кого",
            {
                "fields": ("name", "email", "created_at"),
            },
        ),
        (
            "Повідомлення",
            {
                "fields": ("message",),
            },
        ),
        (
            "Статус",
            {
                "fields": ("status",),
            },
        ),
    )

    _STATUS_COLORS = {
        ConsultationRequest.Status.NEW: ("#dc2626", "#fef2f2"),
        ConsultationRequest.Status.READ: ("#d97706", "#fffbeb"),
        ConsultationRequest.Status.REPLIED: ("#16a34a", "#f0fdf4"),
    }

    @admin.display(description="Статус")
    def status_badge(self, obj):
        color, bg = self._STATUS_COLORS.get(obj.status, ("#6b7280", "#f9fafb"))
        return format_html(
            '<span style="'
            "display:inline-block;padding:2px 10px;border-radius:12px;"
            "font-size:.78rem;font-weight:600;"
            "color:{};background:{};"
            '">{}</span>',
            color,
            bg,
            obj.get_status_display(),
        )

    def get_queryset(self, request):
        return super().get_queryset(request).order_by("-created_at")
