"""Site-wide singleton settings editable from admin."""
from __future__ import annotations

from django.core.exceptions import ValidationError
from django.db import models


class SingletonModel(models.Model):
    """Base for singleton config rows: always pk=1."""

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError("Singleton instances cannot be deleted.")

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class SiteSettings(SingletonModel):
    brand_name_uk = models.CharField("Назва бренду (UA)", max_length=120, default="")
    brand_name_it = models.CharField("Назва бренду (IT)", max_length=120, default="")
    tagline_uk = models.CharField("Підзаголовок (UA)", max_length=240, blank=True, default="")
    tagline_it = models.CharField("Підзаголовок (IT)", max_length=240, blank=True, default="")
    email = models.EmailField("Email", blank=True, default="")
    phone = models.CharField("Телефон", max_length=64, blank=True, default="")
    og_image = models.ImageField("OG-зображення", upload_to="site/", blank=True, null=True)

    class Meta:
        verbose_name = "Налаштування сайту"
        verbose_name_plural = "Налаштування сайту"

    def __str__(self) -> str:
        return self.brand_name_uk or "Site settings"
