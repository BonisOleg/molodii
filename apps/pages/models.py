"""Content models for the public pages."""
from __future__ import annotations

from django.db import models

from apps.core.models import SingletonModel


class HomePage(SingletonModel):
    hero_title_uk = models.CharField("Заголовок героя (UA)", max_length=200, default="")
    hero_title_it = models.CharField("Заголовок героя (IT)", max_length=200, default="")
    hero_subtitle_uk = models.CharField("Підзаголовок (UA)", max_length=300, blank=True, default="")
    hero_subtitle_it = models.CharField("Підзаголовок (IT)", max_length=300, blank=True, default="")
    hero_cta_uk = models.CharField("Текст кнопки (UA)", max_length=80, default="Записатися")
    hero_cta_it = models.CharField("Текст кнопки (IT)", max_length=80, default="Prenota")
    hero_image = models.ImageField("Фото героя", upload_to="home/", blank=True, null=True)

    positioning_uk = models.TextField("Позиціонування (UA)", blank=True, default="")
    positioning_it = models.TextField("Позиціонування (IT)", blank=True, default="")

    about_teaser_uk = models.TextField("Тизер «Про мене» (UA)", blank=True, default="")
    about_teaser_it = models.TextField("Тизер «Про мене» (IT)", blank=True, default="")
    about_image = models.ImageField("Фото для тизера «Про мене»", upload_to="home/", blank=True, null=True)

    services_intro_uk = models.TextField("Тизер «З чим працюю» (UA)", blank=True, default="")
    services_intro_it = models.TextField("Тизер «З чим працюю» (IT)", blank=True, default="")

    therapy_intro_uk = models.TextField("Тизер «Як проходять зустрічі» (UA)", blank=True, default="")
    therapy_intro_it = models.TextField("Тизер «Як проходять зустрічі» (IT)", blank=True, default="")

    contacts_teaser_uk = models.TextField("Тизер «Контакти» (UA)", blank=True, default="")
    contacts_teaser_it = models.TextField("Тизер «Контакти» (IT)", blank=True, default="")

    class Meta:
        verbose_name = "Головна сторінка"
        verbose_name_plural = "Головна сторінка"

    def __str__(self) -> str:
        return "Головна"


class AboutPage(SingletonModel):
    title_uk = models.CharField("Заголовок (UA)", max_length=200, default="Про мене")
    title_it = models.CharField("Заголовок (IT)", max_length=200, default="Su di me")
    lead_uk = models.TextField("Лід (UA)", blank=True, default="")
    lead_it = models.TextField("Лід (IT)", blank=True, default="")
    body_uk = models.TextField("Основний текст (UA)", blank=True, default="")
    body_it = models.TextField("Основний текст (IT)", blank=True, default="")
    education_uk = models.TextField("Освіта (UA)", blank=True, default="")
    education_it = models.TextField("Освіта (IT)", blank=True, default="")
    approach_uk = models.TextField("Підхід (UA)", blank=True, default="")
    approach_it = models.TextField("Підхід (IT)", blank=True, default="")
    photo = models.ImageField("Фото", upload_to="about/", blank=True, null=True)

    class Meta:
        verbose_name = "Про мене"
        verbose_name_plural = "Про мене"

    def __str__(self) -> str:
        return self.title_uk or "Про мене"


class ServicesPage(SingletonModel):
    title_uk = models.CharField("Заголовок (UA)", max_length=200, default="З чим я працюю")
    title_it = models.CharField("Заголовок (IT)", max_length=200, default="Con cosa lavoro")
    intro_uk = models.TextField("Вступ (UA)", blank=True, default="")
    intro_it = models.TextField("Вступ (IT)", blank=True, default="")
    outro_uk = models.TextField("Закриваючий текст (UA)", blank=True, default="")
    outro_it = models.TextField("Закриваючий текст (IT)", blank=True, default="")

    class Meta:
        verbose_name = "З чим я працюю"
        verbose_name_plural = "З чим я працюю"

    def __str__(self) -> str:
        return self.title_uk


class ServiceItem(models.Model):
    page = models.ForeignKey(ServicesPage, related_name="items", on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField("Порядок", default=0)
    title_uk = models.CharField("Назва (UA)", max_length=160)
    title_it = models.CharField("Назва (IT)", max_length=160, blank=True, default="")
    description_uk = models.TextField("Опис (UA)", blank=True, default="")
    description_it = models.TextField("Опис (IT)", blank=True, default="")

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Тема роботи"
        verbose_name_plural = "Теми роботи"

    def __str__(self) -> str:
        return self.title_uk


class TherapyPage(SingletonModel):
    title_uk = models.CharField("Заголовок (UA)", max_length=200, default="Як проходять зустрічі")
    title_it = models.CharField("Заголовок (IT)", max_length=200, default="Come procedono gli incontri")
    intro_uk = models.TextField("Вступ (UA)", blank=True, default="")
    intro_it = models.TextField("Вступ (IT)", blank=True, default="")
    format_online_uk = models.TextField("Формат онлайн (UA)", blank=True, default="")
    format_online_it = models.TextField("Формат онлайн (IT)", blank=True, default="")
    format_offline_uk = models.TextField("Формат офлайн (UA)", blank=True, default="")
    format_offline_it = models.TextField("Формат офлайн (IT)", blank=True, default="")
    pricing_note_uk = models.TextField("Тривалість і вартість (UA)", blank=True, default="")
    pricing_note_it = models.TextField("Тривалість і вартість (IT)", blank=True, default="")
    image = models.ImageField("Фото", upload_to="therapy/", blank=True, null=True)

    class Meta:
        verbose_name = "Як проходять зустрічі"
        verbose_name_plural = "Як проходять зустрічі"

    def __str__(self) -> str:
        return self.title_uk


class TherapyStep(models.Model):
    page = models.ForeignKey(TherapyPage, related_name="steps", on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField("Крок", default=0)
    title_uk = models.CharField("Назва (UA)", max_length=160)
    title_it = models.CharField("Назва (IT)", max_length=160, blank=True, default="")
    body_uk = models.TextField("Опис (UA)", blank=True, default="")
    body_it = models.TextField("Опис (IT)", blank=True, default="")

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Крок роботи"
        verbose_name_plural = "Кроки роботи"

    def __str__(self) -> str:
        return f"{self.order}. {self.title_uk}"
