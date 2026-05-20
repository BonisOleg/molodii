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


class UILabels(SingletonModel):
    """All hardcoded UI strings editable from admin."""

    # Navigation
    nav_skip_uk = models.CharField("Пропустити до контенту (UA)", max_length=80, default="Перейти до контенту")
    nav_skip_it = models.CharField("Пропустити до контенту (IT)", max_length=80, default="Vai al contenuto")
    nav_toggle_uk = models.CharField("Відкрити меню (UA)", max_length=60, default="Відкрити меню")
    nav_toggle_it = models.CharField("Відкрити меню (IT)", max_length=60, default="Apri menu")
    nav_home_uk = models.CharField("Пункт «Головна» (UA)", max_length=60, default="Головна")
    nav_home_it = models.CharField("Пункт «Головна» (IT)", max_length=60, default="Home")
    nav_about_uk = models.CharField("Пункт «Про мене» (UA)", max_length=60, default="Про мене")
    nav_about_it = models.CharField("Пункт «Про мене» (IT)", max_length=60, default="Su di me")
    nav_services_uk = models.CharField("Пункт «З чим я працюю» (UA)", max_length=80, default="З чим я працюю")
    nav_services_it = models.CharField("Пункт «З чим я працюю» (IT)", max_length=80, default="Con cosa lavoro")
    nav_therapy_uk = models.CharField("Пункт «Зустрічі» (UA)", max_length=80, default="Як проходять зустрічі")
    nav_therapy_it = models.CharField("Пункт «Зустрічі» (IT)", max_length=80, default="Gli incontri")
    nav_contacts_uk = models.CharField("Пункт «Контакти» (UA)", max_length=60, default="Контакти")
    nav_contacts_it = models.CharField("Пункт «Контакти» (IT)", max_length=60, default="Contatti")

    # Footer marquee
    footer_format_uk = models.CharField("Футер: формат (UA)", max_length=80, default="Онлайн і офлайн")
    footer_format_it = models.CharField("Футер: формат (IT)", max_length=80, default="Online & di persona")
    footer_intro_uk = models.CharField("Футер: перша розмова (UA)", max_length=80, default="Перша розмова")
    footer_intro_it = models.CharField("Футер: перша розмова (IT)", max_length=80, default="Conversazione di prova")
    footer_lang_badge = models.CharField("Футер: бейдж мов (UA · IT)", max_length=20, default="UA · IT")
    footer_credit_uk = models.CharField("Футер: підпис розробника (UA)", max_length=80, default="Розроблено в PrometeyLabs")
    footer_credit_it = models.CharField("Футер: підпис розробника (IT)", max_length=80, default="Sviluppato da PrometeyLabs")
    footer_credit_url = models.CharField("Футер: URL розробника", max_length=200, blank=True, default="https://www.prometeylabs.com/")

    # Hero section
    hero_meta_uk = models.CharField("Hero: рядок формату (UA)", max_length=120, default="Онлайн та вживу (Мілан, Комо)")
    hero_meta_it = models.CharField("Hero: рядок формату (IT)", max_length=120, default="Online e di persona (Milano, Como)")
    hero_badge_uk = models.CharField("Hero: бейдж слотів (UA)", max_length=60, default="Є вільні слоти")
    hero_badge_it = models.CharField("Hero: бейдж слотів (IT)", max_length=60, default="Posti disponibili")
    hero_about_link_uk = models.CharField("Hero: посилання «Про мене» (UA)", max_length=60, default="Про мене")
    hero_about_link_it = models.CharField("Hero: посилання «Про мене» (IT)", max_length=60, default="Su di me")

    # About section
    about_tag_uk = models.CharField("Про мене: тег секції (UA)", max_length=60, default="Про мене")
    about_tag_it = models.CharField("Про мене: тег секції (IT)", max_length=60, default="Su di me")
    about_eyebrow_uk = models.CharField("Про мене: eyebrow (UA)", max_length=80, default="Знайомство")
    about_eyebrow_it = models.CharField("Про мене: eyebrow (IT)", max_length=80, default="Conosciamoci")
    about_read_more_uk = models.CharField("Про мене: посилання «Читати далі» (UA)", max_length=60, default="Читати далі –")
    about_read_more_it = models.CharField("Про мене: посилання «Читати далі» (IT)", max_length=60, default="Leggi di più")
    about_contact_link_uk = models.CharField("Про мене: посилання «Написати» (UA)", max_length=60, default="Написати мені")
    about_contact_link_it = models.CharField("Про мене: посилання «Написати» (IT)", max_length=60, default="Scrivimi")
    about_edu_num_uk = models.CharField("Картка «Освіта»: номер (UA)", max_length=40, default="01 — Освіта")
    about_edu_num_it = models.CharField("Картка «Освіта»: номер (IT)", max_length=40, default="01 — Background")
    about_edu_title_uk = models.CharField("Картка «Освіта»: назва (UA)", max_length=60, default="Освіта")
    about_edu_title_it = models.CharField("Картка «Освіта»: назва (IT)", max_length=60, default="Formazione")
    about_approach_num_uk = models.CharField("Картка «Підхід»: номер (UA)", max_length=40, default="02 — Метод")
    about_approach_num_it = models.CharField("Картка «Підхід»: номер (IT)", max_length=40, default="02 — Metodo")
    about_approach_title_uk = models.CharField("Картка «Підхід»: назва (UA)", max_length=60, default="Підхід")
    about_approach_title_it = models.CharField("Картка «Підхід»: назва (IT)", max_length=60, default="Approccio")

    # Services section
    services_eyebrow_uk = models.CharField("З чим я працюю: eyebrow (UA)", max_length=80, default="З чим я працюю")
    services_eyebrow_it = models.CharField("З чим я працюю: eyebrow (IT)", max_length=80, default="Con cosa lavoro")
    services_empty_uk = models.CharField("З чим я працюю: порожній стан (UA)", max_length=120, default="Розділ у підготовці.")
    services_empty_it = models.CharField("З чим я працюю: порожній стан (IT)", max_length=120, default="Sezione in preparazione.")
    services_cta_uk = models.CharField("З чим я працюю: кнопка CTA (UA)", max_length=80, default="Записатися на консультацію")
    services_cta_it = models.CharField("З чим я працюю: кнопка CTA (IT)", max_length=80, default="Prenota una consulenza")

    # Therapy section
    therapy_eyebrow_uk = models.CharField("Зустрічі: eyebrow (UA)", max_length=80, default="Як проходить робота")
    therapy_eyebrow_it = models.CharField("Зустрічі: eyebrow (IT)", max_length=80, default="Come lavoriamo")
    therapy_steps_eyebrow_uk = models.CharField("Зустрічі: eyebrow кроків (UA)", max_length=60, default="Шлях")
    therapy_steps_eyebrow_it = models.CharField("Зустрічі: eyebrow кроків (IT)", max_length=60, default="Il percorso")
    therapy_steps_title_uk = models.CharField("Зустрічі: заголовок кроків (UA)", max_length=80, default="Як ми будемо працювати")
    therapy_steps_title_it = models.CharField("Зустрічі: заголовок кроків (IT)", max_length=80, default="Come si svolge")
    therapy_pricing_eyebrow_uk = models.CharField("Зустрічі: eyebrow вартості (UA)", max_length=60, default="Практика")
    therapy_pricing_eyebrow_it = models.CharField("Зустрічі: eyebrow вартості (IT)", max_length=60, default="Pratica")
    therapy_pricing_title_uk = models.CharField("Зустрічі: заголовок вартості (UA)", max_length=80, default="Тривалість і вартість")
    therapy_pricing_title_it = models.CharField("Зустрічі: заголовок вартості (IT)", max_length=80, default="Durata e tariffe")
    therapy_pricing_subtitle_uk = models.CharField("Зустрічі: підзаголовок вартості (UA)", max_length=60, default="Одна сесія")
    therapy_pricing_subtitle_it = models.CharField("Зустрічі: підзаголовок вартості (IT)", max_length=60, default="Sessione singola")
    therapy_cta_uk = models.CharField("Зустрічі: кнопка CTA (UA)", max_length=60, default="Записатися")
    therapy_cta_it = models.CharField("Зустрічі: кнопка CTA (IT)", max_length=60, default="Prenota")

    # Contacts section
    contacts_eyebrow_uk = models.CharField("Контакти: eyebrow (UA)", max_length=60, default="Контакти")
    contacts_eyebrow_it = models.CharField("Контакти: eyebrow (IT)", max_length=60, default="Contatti")
    contacts_phone_uk = models.CharField("Контакти: підпис телефону (UA)", max_length=40, default="Телефон")
    contacts_phone_it = models.CharField("Контакти: підпис телефону (IT)", max_length=40, default="Telefono")
    contacts_hours_uk = models.CharField("Контакти: підпис графіку (UA)", max_length=40, default="Графік")
    contacts_hours_it = models.CharField("Контакти: підпис графіку (IT)", max_length=40, default="Orari")
    contacts_offices_eyebrow_uk = models.CharField("Контакти: eyebrow кабінетів (UA)", max_length=60, default="Адреси")
    contacts_offices_eyebrow_it = models.CharField("Контакти: eyebrow кабінетів (IT)", max_length=60, default="Indirizzi")
    contacts_offices_title_uk = models.CharField("Контакти: назва секції кабінетів (UA)", max_length=60, default="Кабінети")
    contacts_offices_title_it = models.CharField("Контакти: назва секції кабінетів (IT)", max_length=60, default="I miei studi")
    contacts_map_link_uk = models.CharField("Контакти: посилання на карту (UA)", max_length=60, default="Відкрити на карті")
    contacts_map_link_it = models.CharField("Контакти: посилання на карту (IT)", max_length=60, default="Apri sulla mappa")
    contacts_email_uk = models.CharField("Контакти: підпис Email (UA)", max_length=40, default="Email")
    contacts_email_it = models.CharField("Контакти: підпис Email (IT)", max_length=40, default="Email")

    # Contact form
    form_name_uk = models.CharField("Форма: поле «Ім'я» (UA)", max_length=40, default="Ім'я")
    form_name_it = models.CharField("Форма: поле «Ім'я» (IT)", max_length=40, default="Nome")
    form_email_uk = models.CharField("Форма: поле «Email» (UA)", max_length=40, default="Email")
    form_email_it = models.CharField("Форма: поле «Email» (IT)", max_length=40, default="Email")
    form_message_uk = models.CharField("Форма: поле «Повідомлення» (UA)", max_length=60, default="Повідомлення")
    form_message_it = models.CharField("Форма: поле «Повідомлення» (IT)", max_length=60, default="Messaggio")
    form_submit_uk = models.CharField("Форма: кнопка «Надіслати» (UA)", max_length=40, default="Надіслати")
    form_submit_it = models.CharField("Форма: кнопка «Надіслати» (IT)", max_length=40, default="Invia")
    form_success_uk = models.CharField("Форма: повідомлення про успіх (UA)", max_length=200, default="Дякую! Я відповім вам найближчим часом.")
    form_success_it = models.CharField("Форма: повідомлення про успіх (IT)", max_length=200, default="Grazie! Ti risponderò al più presto.")

    class Meta:
        verbose_name = "Написи інтерфейсу"
        verbose_name_plural = "Написи інтерфейсу"

    def __str__(self) -> str:
        return "Написи інтерфейсу"
