"""Pages admin: all singletons + inlines with Unfold theme."""
from __future__ import annotations

from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin, StackedInline, TabularInline

from apps.core.admin import SingletonAdmin

from .models import (
    AboutPage,
    HomePage,
    ServiceItem,
    ServicesPage,
    TherapyPage,
    TherapyStep,
)


@admin.register(HomePage)
class HomePageAdmin(SingletonAdmin):
    compressed_fields = True
    readonly_fields = ("hero_image_preview", "about_image_preview")

    fieldsets = (
        (
            "Hero-секція",
            {
                "fields": (
                    "hero_title_uk",
                    "hero_title_it",
                    "hero_subtitle_uk",
                    "hero_subtitle_it",
                    "hero_cta_uk",
                    "hero_cta_it",
                    "hero_image",
                    "hero_image_preview",
                ),
                "classes": ["tab"],
            },
        ),
        (
            "Позиціонування",
            {
                "fields": ("positioning_uk", "positioning_it"),
                "classes": ["tab"],
            },
        ),
        (
            "Тизер «Про мене»",
            {
                "fields": (
                    "about_teaser_uk",
                    "about_teaser_it",
                    "about_image",
                    "about_image_preview",
                ),
                "classes": ["tab"],
            },
        ),
        (
            "Тизер «З чим працюю»",
            {
                "fields": ("services_intro_uk", "services_intro_it"),
                "classes": ["tab"],
            },
        ),
        (
            "Тизер «Як проходять зустрічі»",
            {
                "fields": ("therapy_intro_uk", "therapy_intro_it"),
                "classes": ["tab"],
            },
        ),
        (
            "Тизер «Контакти»",
            {
                "fields": ("contacts_teaser_uk", "contacts_teaser_it"),
                "classes": ["tab"],
            },
        ),
    )

    @admin.display(description="Прев'ю hero-фото")
    def hero_image_preview(self, obj):
        if obj and obj.hero_image:
            return format_html(
                '<img src="{}" style="max-height:120px;border-radius:6px;" />',
                obj.hero_image.url,
            )
        return "—"

    @admin.display(description="Прев'ю фото тизера")
    def about_image_preview(self, obj):
        if obj and obj.about_image:
            return format_html(
                '<img src="{}" style="max-height:120px;border-radius:6px;" />',
                obj.about_image.url,
            )
        return "—"


@admin.register(AboutPage)
class AboutPageAdmin(SingletonAdmin):
    compressed_fields = True
    readonly_fields = ("photo_preview",)

    fieldsets = (
        (
            "Заголовок і лід",
            {
                "fields": (
                    "title_uk",
                    "title_it",
                    "lead_uk",
                    "lead_it",
                    "photo",
                    "photo_preview",
                ),
                "classes": ["tab"],
            },
        ),
        (
            "Основний текст",
            {
                "fields": ("body_uk", "body_it"),
                "classes": ["tab"],
            },
        ),
        (
            "Освіта",
            {
                "fields": ("education_uk", "education_it"),
                "classes": ["tab"],
            },
        ),
        (
            "Підхід",
            {
                "fields": ("approach_uk", "approach_it"),
                "classes": ["tab"],
            },
        ),
    )

    @admin.display(description="Прев'ю фото")
    def photo_preview(self, obj):
        if obj and obj.photo:
            return format_html(
                '<img src="{}" style="max-height:120px;border-radius:6px;" />',
                obj.photo.url,
            )
        return "—"


class ServiceItemInline(TabularInline):
    model = ServiceItem
    extra = 1
    fields = ("order", "title_uk", "title_it", "description_uk", "description_it")
    tab = True


@admin.register(ServicesPage)
class ServicesPageAdmin(SingletonAdmin):
    compressed_fields = True
    inlines = [ServiceItemInline]

    fieldsets = (
        (
            "Сторінка",
            {
                "fields": (
                    "title_uk",
                    "title_it",
                    "intro_uk",
                    "intro_it",
                    "outro_uk",
                    "outro_it",
                ),
                "classes": ["tab"],
            },
        ),
    )


class TherapyStepInline(TabularInline):
    model = TherapyStep
    extra = 1
    fields = ("order", "title_uk", "title_it", "body_uk", "body_it")
    tab = True


@admin.register(TherapyPage)
class TherapyPageAdmin(SingletonAdmin):
    compressed_fields = True
    inlines = [TherapyStepInline]
    readonly_fields = ("image_preview",)

    fieldsets = (
        (
            "Заголовок",
            {
                "fields": (
                    "title_uk",
                    "title_it",
                    "intro_uk",
                    "intro_it",
                    "image",
                    "image_preview",
                ),
                "classes": ["tab"],
            },
        ),
        (
            "Формати",
            {
                "fields": (
                    "format_online_uk",
                    "format_online_it",
                    "format_offline_uk",
                    "format_offline_it",
                ),
                "classes": ["tab"],
            },
        ),
        (
            "Тривалість і вартість",
            {
                "fields": ("pricing_note_uk", "pricing_note_it"),
                "classes": ["tab"],
            },
        ),
    )

    @admin.display(description="Прев'ю фото")
    def image_preview(self, obj):
        if obj and obj.image:
            return format_html(
                '<img src="{}" style="max-height:120px;border-radius:6px;" />',
                obj.image.url,
            )
        return "—"
