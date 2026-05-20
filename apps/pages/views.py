"""Public page views."""
from __future__ import annotations

from django.shortcuts import redirect, render

from apps.contacts.forms import ContactForm
from apps.contacts.models import ContactsPage, SocialLink
from apps.contacts.utils import handle_contact_submission, offices_for_display

from .models import (
    AboutPage,
    HomePage,
    ServicesPage,
    TherapyPage,
)


def home(request):
    page = HomePage.load()
    services_page = ServicesPage.load()
    therapy_page = TherapyPage.load()
    contacts_page = ContactsPage.load()
    lang = getattr(request, "lang", "uk")

    if request.method == "POST":
        form = ContactForm(request.POST, lang=lang)
        if form.is_valid():
            handle_contact_submission(form.cleaned_data, request)
            return redirect(request.path + "?submitted=1#contacts")
    else:
        form = ContactForm(lang=lang)

    submitted = request.GET.get("submitted") == "1"

    return render(request, "pages/home.html", {
        "page": page,
        "about": AboutPage.load(),
        "services": services_page,
        "therapy": therapy_page,
        "contacts_page": contacts_page,
        "items": services_page.items.all(),
        "steps": therapy_page.steps.all(),
        "offices": offices_for_display(),
        "socials": SocialLink.objects.all(),
        "form": form,
        "submitted": submitted,
    })


def about(request):
    return render(request, "pages/about.html", {"page": AboutPage.load()})


def services(request):
    page = ServicesPage.load()
    return render(request, "pages/services.html", {
        "page": page,
        "items": page.items.all(),
    })


def therapy(request):
    page = TherapyPage.load()
    return render(request, "pages/therapy.html", {
        "page": page,
        "steps": page.steps.all(),
    })


def contacts(request):
    page = ContactsPage.load()
    lang = getattr(request, "lang", "uk")

    if request.method == "POST":
        form = ContactForm(request.POST, lang=lang)
        if form.is_valid():
            handle_contact_submission(form.cleaned_data, request)
            return redirect(request.path + "?submitted=1")
    else:
        form = ContactForm(lang=lang)

    submitted = request.GET.get("submitted") == "1"

    return render(request, "contacts/contacts.html", {
        "page": page,
        "offices": offices_for_display(),
        "socials": SocialLink.objects.all(),
        "form": form,
        "submitted": submitted,
    })
