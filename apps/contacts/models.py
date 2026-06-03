"""Contacts page, offices, social links and consultation requests."""
from __future__ import annotations

from django.db import models
from django.utils import timezone

from apps.core.models import SingletonModel

CERNOBBIO_GALLERY_STATIC = (
    "img/offices/cernobbio/interior-01.jpg",
    "img/offices/cernobbio/interior-02.jpg",
)
MILAN_GALLERY_STATIC = (
    "img/offices/milan/interior-01.jpg",
    "img/offices/milan/interior-02.jpg",
)


class ContactsPage(SingletonModel):
    title_uk = models.CharField("Заголовок (UA)", max_length=200, default="Контакти")
    title_it = models.CharField("Заголовок (IT)", max_length=200, default="Contatti")
    intro_uk = models.TextField("Вступ (UA)", blank=True, default="")
    intro_it = models.TextField("Вступ (IT)", blank=True, default="")
    working_hours_uk = models.TextField("Графік (UA)", blank=True, default="")
    working_hours_it = models.TextField("Графік (IT)", blank=True, default="")

    class Meta:
        verbose_name = "Сторінка «Контакти»"
        verbose_name_plural = "Сторінка «Контакти»"

    def __str__(self) -> str:
        return self.title_uk


class Office(models.Model):
    city_uk = models.CharField("Місто (UA)", max_length=120)
    city_it = models.CharField("Місто (IT)", max_length=120, blank=True, default="")
    address_uk = models.CharField("Адреса (UA)", max_length=255)
    address_it = models.CharField("Адреса (IT)", max_length=255, blank=True, default="")
    map_url = models.URLField("Посилання на карту", blank=True, default="")
    photo = models.ImageField("Фото кабінету", upload_to="offices/", blank=True, null=True)
    order = models.PositiveSmallIntegerField("Порядок", default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Кабінет"
        verbose_name_plural = "Кабінети"

    def __str__(self) -> str:
        return f"{self.city_uk} — {self.address_uk}"

    @property
    def gallery_image_urls(self) -> list[str]:
        """Bundled static photos for known offices; optional admin upload for others."""
        from django.templatetags.static import static

        if "Monti" in self.address_uk:
            return [static(path) for path in CERNOBBIO_GALLERY_STATIC]
        if "Camelie" in self.address_uk:
            return [static(path) for path in MILAN_GALLERY_STATIC]

        urls: list[str] = []
        prefetched = getattr(self, "_prefetched_objects_cache", {}).get("photos")
        photos = (
            sorted(prefetched, key=lambda p: (p.order, p.pk))
            if prefetched is not None
            else self.photos.order_by("order", "pk")
        )
        for photo in photos:
            if not photo.image:
                continue
            try:
                if photo.image.storage.exists(photo.image.name):
                    urls.append(photo.image.url)
            except (ValueError, OSError):
                continue
        if urls:
            return urls
        if self.photo:
            try:
                if self.photo.storage.exists(self.photo.name):
                    return [self.photo.url]
            except (ValueError, OSError):
                pass
        return []


class OfficePhoto(models.Model):
    office = models.ForeignKey(
        Office,
        on_delete=models.CASCADE,
        related_name="photos",
        verbose_name="Кабінет",
    )
    image = models.ImageField("Фото", upload_to="offices/")
    order = models.PositiveSmallIntegerField("Порядок", default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Фото кабінету"
        verbose_name_plural = "Фото кабінетів"

    def __str__(self) -> str:
        return f"{self.office.city_uk} — фото #{self.order + 1}"


class SocialLink(models.Model):
    class Platform(models.TextChoices):
        INSTAGRAM = "instagram", "Instagram"
        LINKEDIN = "linkedin", "LinkedIn"
        FACEBOOK = "facebook", "Facebook"
        TELEGRAM = "telegram", "Telegram"
        WHATSAPP = "whatsapp", "WhatsApp"
        EMAIL = "email", "Email"

    platform = models.CharField("Платформа", max_length=20, choices=Platform.choices)
    url = models.URLField("Посилання")
    order = models.PositiveSmallIntegerField("Порядок", default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Соц. посилання"
        verbose_name_plural = "Соц. посилання"
        constraints = [
            models.UniqueConstraint(fields=["platform"], name="unique_social_platform"),
        ]

    def __str__(self) -> str:
        return self.get_platform_display()


class ConsultationRequest(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "Новий"
        READ = "read", "Прочитано"
        REPLIED = "replied", "Відповіли"

    name = models.CharField("Ім'я", max_length=120)
    email = models.EmailField("Email")
    message = models.TextField("Повідомлення")
    status = models.CharField(
        "Статус",
        max_length=10,
        choices=Status.choices,
        default=Status.NEW,
        db_index=True,
    )
    created_at = models.DateTimeField("Дата", default=timezone.now, db_index=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Запит на консультацію"
        verbose_name_plural = "Запити на консультацію"

    def __str__(self) -> str:
        return f"{self.name} <{self.email}> — {self.created_at:%d.%m.%Y %H:%M}"
