"""Contact form with honeypot and basic anti-bot measures."""
from __future__ import annotations

from django import forms
from django.core.exceptions import ValidationError

_ERRORS: dict[str, dict[str, str]] = {
    "uk": {
        "required": "Це поле обов'язкове.",
        "email_invalid": "Введіть правильну адресу електронної пошти.",
        "max_length": "Текст занадто довгий.",
        "message_too_short": "Повідомлення занадто коротке.",
    },
    "it": {
        "required": "Questo campo è obbligatorio.",
        "email_invalid": "Inserisci un indirizzo email valido.",
        "max_length": "Il testo è troppo lungo.",
        "message_too_short": "Il messaggio è troppo corto.",
    },
}


class ContactForm(forms.Form):
    name = forms.CharField(
        label="",
        max_length=120,
        widget=forms.TextInput(attrs={"autocomplete": "name", "class": "form__input"}),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"autocomplete": "email", "class": "form__input"}),
    )
    message = forms.CharField(
        label="",
        widget=forms.Textarea(attrs={"rows": 5, "class": "form__input form__input--textarea"}),
        max_length=4000,
    )
    company = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(attrs={"tabindex": "-1", "autocomplete": "off", "class": "form__honeypot"}),
    )

    def __init__(self, *args, lang: str = "uk", **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._lang = lang
        err = _ERRORS.get(lang, _ERRORS["uk"])
        for field in self.fields.values():
            field.error_messages["required"] = err["required"]
            if "invalid" in field.error_messages:
                field.error_messages["invalid"] = err["email_invalid"]
            if "max_length" in field.error_messages:
                field.error_messages["max_length"] = err["max_length"]

    def clean_company(self) -> str:
        value = self.cleaned_data.get("company", "")
        if value:
            raise ValidationError("Bot detected.")
        return value

    def clean_message(self) -> str:
        message = self.cleaned_data.get("message", "").strip()
        if len(message) < 5:
            raise ValidationError(_ERRORS.get(self._lang, _ERRORS["uk"])["message_too_short"])
        return message
