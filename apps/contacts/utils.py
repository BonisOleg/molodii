"""Helpers for contact form processing."""
from __future__ import annotations

import logging

from django.conf import settings
from django.core.mail import EmailMessage

from .models import ConsultationRequest

logger = logging.getLogger(__name__)


def handle_contact_submission(data: dict, request) -> None:
    """Save request to DB and send email notification.

    DB write always happens. Email failure is logged and swallowed so
    the user always sees a success state.
    """
    ConsultationRequest.objects.create(
        name=data["name"],
        email=data["email"],
        message=data["message"],
    )

    subject = f"[Сайт] Нове повідомлення від {data['name']}"
    body = (
        f"Ім'я: {data['name']}\n"
        f"Email: {data['email']}\n\n"
        f"Повідомлення:\n{data['message']}\n"
    )
    try:
        EmailMessage(
            subject=subject,
            body=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.CONTACT_RECIPIENT],
            reply_to=[data["email"]],
        ).send(fail_silently=False)
    except Exception:
        logger.exception("Failed to deliver contact form email")
