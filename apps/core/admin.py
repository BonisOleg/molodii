"""Core admin: SiteSettings and UILabels singletons with Unfold theme."""
from __future__ import annotations

from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from .models import SiteSettings, UILabels


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


@admin.register(UILabels)
class UILabelsAdmin(SingletonAdmin):
    compressed_fields = True

    fieldsets = (
        (
            "Навігація",
            {
                "fields": (
                    "nav_skip_uk", "nav_skip_it",
                    "nav_toggle_uk", "nav_toggle_it",
                    "nav_home_uk", "nav_home_it",
                    "nav_about_uk", "nav_about_it",
                    "nav_services_uk", "nav_services_it",
                    "nav_therapy_uk", "nav_therapy_it",
                    "nav_contacts_uk", "nav_contacts_it",
                ),
                "classes": ["tab"],
            },
        ),
        (
            "Футер",
            {
                "fields": (
                    "footer_format_uk", "footer_format_it",
                    "footer_intro_uk", "footer_intro_it",
                    "footer_lang_badge",
                    "footer_credit_uk", "footer_credit_it",
                    "footer_credit_url",
                ),
                "classes": ["tab"],
            },
        ),
        (
            "Hero-секція",
            {
                "fields": (
                    "hero_meta_uk", "hero_meta_it",
                    "hero_badge_uk", "hero_badge_it",
                    "hero_about_link_uk", "hero_about_link_it",
                ),
                "classes": ["tab"],
            },
        ),
        (
            "Секція «Про мене»",
            {
                "fields": (
                    "about_tag_uk", "about_tag_it",
                    "about_eyebrow_uk", "about_eyebrow_it",
                    "about_read_more_uk", "about_read_more_it",
                    "about_contact_link_uk", "about_contact_link_it",
                    "about_edu_num_uk", "about_edu_num_it",
                    "about_edu_title_uk", "about_edu_title_it",
                    "about_approach_num_uk", "about_approach_num_it",
                    "about_approach_title_uk", "about_approach_title_it",
                ),
                "classes": ["tab"],
            },
        ),
        (
            "Секція «З чим я працюю»",
            {
                "fields": (
                    "services_eyebrow_uk", "services_eyebrow_it",
                    "services_empty_uk", "services_empty_it",
                    "services_cta_uk", "services_cta_it",
                ),
                "classes": ["tab"],
            },
        ),
        (
            "Секція «Як проходять зустрічі»",
            {
                "fields": (
                    "therapy_eyebrow_uk", "therapy_eyebrow_it",
                    "therapy_steps_eyebrow_uk", "therapy_steps_eyebrow_it",
                    "therapy_steps_title_uk", "therapy_steps_title_it",
                    "therapy_pricing_eyebrow_uk", "therapy_pricing_eyebrow_it",
                    "therapy_pricing_title_uk", "therapy_pricing_title_it",
                    "therapy_pricing_subtitle_uk", "therapy_pricing_subtitle_it",
                    "therapy_cta_uk", "therapy_cta_it",
                ),
                "classes": ["tab"],
            },
        ),
        (
            "Секція «Контакти»",
            {
                "fields": (
                    "contacts_eyebrow_uk", "contacts_eyebrow_it",
                    "contacts_phone_uk", "contacts_phone_it",
                    "contacts_hours_uk", "contacts_hours_it",
                    "contacts_offices_eyebrow_uk", "contacts_offices_eyebrow_it",
                    "contacts_offices_title_uk", "contacts_offices_title_it",
                    "contacts_map_link_uk", "contacts_map_link_it",
                    "contacts_email_uk", "contacts_email_it",
                ),
                "classes": ["tab"],
            },
        ),
        (
            "Форма зворотного зв'язку",
            {
                "fields": (
                    "form_name_uk", "form_name_it",
                    "form_email_uk", "form_email_it",
                    "form_message_uk", "form_message_it",
                    "form_submit_uk", "form_submit_it",
                    "form_success_uk", "form_success_it",
                ),
                "classes": ["tab"],
            },
        ),
    )
