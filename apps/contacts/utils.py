"""Helpers for contact form processing."""
from __future__ import annotations

import logging

from django.conf import settings
from django.core.mail import EmailMessage

logger = logging.getLogger(__name__)


def handle_contact_submission(data: dict, request) -> None:
    """Send email notification with the form payload.

    Failures are logged and silently swallowed so the user always sees a
    success state — duplicate notifications are mitigated by rate-limit.
    """
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
