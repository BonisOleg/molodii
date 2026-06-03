"""Smoke tests for public pages and i18n machinery."""
from __future__ import annotations

import pytest
from django.test import Client, override_settings
from django.core import mail
from django.template import Context, Template

from apps.core.models import SiteSettings
from apps.core.templatetags.i18n_fields import md_links
from apps.pages.about_content import (
    APPROACH_UK,
    EDUCATION_UK,
    OPL_URL,
    PSY_URL,
    approach_has_raw_url,
    education_has_raw_url,
)
from apps.pages.models import (
    AboutPage, HomePage, ServiceItem, ServicesPage, TherapyPage,
)
from apps.pages.services_content import SERVICE_ITEMS_UK, SERVICES_OUTRO_UK
from apps.contacts.models import ContactsPage


@pytest.fixture(autouse=True)
def _seed(db):
    SiteSettings.load()
    home = HomePage.load()
    home.hero_title_uk = "Простір спокою"
    home.hero_title_it = "Spazio di calma"
    home.save()

    about = AboutPage.load(); about.title_uk = "Про мене"; about.title_it = "Su di me"; about.save()
    services = ServicesPage.load(); services.title_uk = "З чим"; services.title_it = "Con cosa"; services.save()
    therapy = TherapyPage.load(); therapy.title_uk = "Терапія"; therapy.title_it = "Terapia"; therapy.save()
    contacts = ContactsPage.load(); contacts.title_uk = "Контакти"; contacts.title_it = "Contatti"; contacts.save()


@pytest.mark.parametrize("path,needle", [
    ("/", "Простір спокою"),
    ("/about/", "Про мене"),
    ("/services/", "З чим"),
    ("/therapy/", "Терапія"),
    ("/contacts/", "Контакти"),
])
def test_uk_pages_render(client: Client, path: str, needle: str):
    resp = client.get(path)
    assert resp.status_code == 200
    assert needle in resp.content.decode("utf-8")


@pytest.mark.parametrize("path,needle", [
    ("/it/", "Spazio di calma"),
    ("/it/about/", "Su di me"),
    ("/it/services/", "Con cosa"),
    ("/it/therapy/", "Terapia"),
    ("/it/contacts/", "Contatti"),
])
def test_it_pages_render(client: Client, path: str, needle: str):
    resp = client.get(path)
    assert resp.status_code == 200
    assert needle in resp.content.decode("utf-8")


def test_t_tag_falls_back_to_uk():
    page = HomePage.load()
    page.hero_title_uk = "UA"
    page.hero_title_it = ""
    page.save()
    tpl = Template("{% load i18n_fields %}{% t page 'hero_title' %}")
    assert tpl.render(Context({"page": page, "LANG": "it"})) == "UA"


def test_md_links_renders_inline_anchor():
    result = str(md_links(f"Текст [орден]({OPL_URL}) далі."))
    assert f'<a href="{OPL_URL}"' in result
    assert "орден</a>" in result
    assert OPL_URL not in result.replace(f'href="{OPL_URL}"', "")


def test_about_raw_url_helpers():
    assert not education_has_raw_url(EDUCATION_UK)
    assert education_has_raw_url(f"Освіта. {OPL_URL}")
    assert not approach_has_raw_url(APPROACH_UK)
    assert approach_has_raw_url(f"Кодекс {PSY_URL} далі.")


def test_home_about_cards_render_inline_links(client: Client):
    about = AboutPage.load()
    about.education_uk = EDUCATION_UK
    about.approach_uk = APPROACH_UK
    about.save(update_fields=["education_uk", "approach_uk"])

    html = client.get("/").content.decode("utf-8")
    assert f'<a href="{OPL_URL}"' in html
    assert f'<a href="{PSY_URL}"' in html
    assert "Зареєстрована в ордені психологів Ломбардії" in html
    assert "етичного кодексу італійських психологів" in html


def test_bundled_static_images_on_home(client: Client):
    resp = client.get("/")
    html = resp.content.decode("utf-8")
    assert "img/seed/hero" in html
    assert "img/seed/about" in html


def test_contacts_office_static_gallery(client: Client):
    resp = client.get("/contacts/")
    html = resp.content.decode("utf-8")
    assert "img/offices/milan/" in html
    assert "img/offices/cernobbio/" in html


def test_services_page_renders_bullet_list(client: Client):
    page = ServicesPage.load()
    page.intro_uk = "Ви можете звернутися до мене, якщо відчуваєте:"
    page.outro_uk = SERVICES_OUTRO_UK
    page.save(update_fields=["intro_uk", "outro_uk"])

    page.items.all().delete()
    for i, title in enumerate(SERVICE_ITEMS_UK):
        ServiceItem.objects.create(page=page, order=i, title_uk=title, title_it="")

    html = client.get("/services/").content.decode("utf-8")
    assert "труднощі адаптації до нової країни" in html
    assert "тривожні або депресивні стани" in html
    assert "Напишіть мені для того щоб дізнатись вартість зустрічей." in html
    assert "Тривога і панічні атаки" not in html
    assert 'class="services-list"' in html


def test_healthz(client: Client):
    resp = client.get("/healthz")
    assert resp.status_code == 200
    assert resp.content == b"ok"


def test_lang_middleware_sets_request_lang(client: Client):
    resp = client.get("/it/")
    assert resp.status_code == 200
    resp_uk = client.get("/")
    assert resp_uk.status_code == 200


def test_contact_form_honeypot_blocks_bot(client: Client):
    resp = client.post("/contacts/", data={
        "name": "Bot",
        "email": "bot@example.com",
        "message": "Some long enough message",
        "company": "evil-bot-filled-this",
    })
    assert resp.status_code == 200
    assert "submitted=True" not in resp.content.decode("utf-8").replace(" ", "")


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
def test_contact_form_sends_to_notification_email(client: Client):
    site = SiteSettings.load()
    site.notification_email = "notify@example.com"
    site.save(update_fields=["notification_email"])

    client.post("/contacts/", data={
        "name": "Клієнт",
        "email": "client@example.com",
        "message": "Хочу консультацію",
        "company": "",
    })

    assert len(mail.outbox) == 1
    assert mail.outbox[0].to == ["notify@example.com"]


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    CONTACT_RECIPIENT="fallback@example.com",
)
def test_contact_form_falls_back_to_public_email(client: Client):
    site = SiteSettings.load()
    site.email = "public@example.com"
    site.notification_email = ""
    site.save(update_fields=["email", "notification_email"])

    client.post("/contacts/", data={
        "name": "Клієнт",
        "email": "client@example.com",
        "message": "Хочу консультацію",
        "company": "",
    })

    assert len(mail.outbox) == 1
    assert mail.outbox[0].to == ["public@example.com"]


@override_settings(DEBUG=False)
def test_home_uses_static_images_when_media_not_served(client: Client):
    home = HomePage.load()
    home.hero_title_uk = "Заголовок"
    home.hero_image.name = "home/hero.png"
    home.save(update_fields=["hero_title_uk", "hero_image"])

    html = client.get("/").content.decode("utf-8")
    assert "/static/img/seed/hero" in html
    assert "/media/home/hero.png" not in html
