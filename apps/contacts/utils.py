"""Helpers for contact form processing and office listings."""
from __future__ import annotations

import json
import logging
import threading
import time
from typing import Any

from django.conf import settings
from django.core.mail import EmailMessage
from django.db.models import Prefetch

from apps.core.models import SiteSettings

from .models import ConsultationRequest, Office, OfficePhoto

logger = logging.getLogger(__name__)

_DEBUG_LOG = "/Users/olegbonislavskyi/Sites/Психолог /.cursor/debug-d9fc80.log"


def _agent_log(
    location: str,
    message: str,
    data: dict[str, Any],
    hypothesis_id: str,
    run_id: str = "pre-fix",
) -> None:
    # #region agent log
    try:
        with open(_DEBUG_LOG, "a", encoding="utf-8") as log_file:
            log_file.write(
                json.dumps(
                    {
                        "sessionId": "d9fc80",
                        "timestamp": int(time.time() * 1000),
                        "location": location,
                        "message": message,
                        "data": data,
                        "hypothesisId": hypothesis_id,
                        "runId": run_id,
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )
    except OSError:
        pass
    # #endregion


def offices_for_display():
    """Offices with photos prefetched in display order."""
    return Office.objects.prefetch_related(
        Prefetch(
            "photos",
            queryset=OfficePhoto.objects.order_by("order", "id"),
        ),
    )


def _send_contact_notification_email(data: dict, recipient: str) -> None:
    subject = f"[Сайт] Нове повідомлення від {data['name']}"
    body = (
        f"Ім'я: {data['name']}\n"
        f"Email: {data['email']}\n\n"
        f"Повідомлення:\n{data['message']}\n"
    )
    # #region agent log
    email_started = time.perf_counter()
    _agent_log(
        "contacts/utils.py:_send_contact_notification_email",
        "smtp send start",
        {"recipientConfigured": bool(recipient)},
        "A",
    )
    # #endregion
    try:
        EmailMessage(
            subject=subject,
            body=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient],
            reply_to=[data["email"]],
        ).send(fail_silently=False)
        # #region agent log
        _agent_log(
            "contacts/utils.py:_send_contact_notification_email",
            "smtp send done",
            {"elapsedMs": int((time.perf_counter() - email_started) * 1000)},
            "A",
        )
        # #endregion
    except Exception as exc:
        # #region agent log
        _agent_log(
            "contacts/utils.py:_send_contact_notification_email",
            "smtp send failed",
            {
                "elapsedMs": int((time.perf_counter() - email_started) * 1000),
                "errorType": type(exc).__name__,
            },
            "A",
        )
        # #endregion
        logger.exception("Failed to deliver contact form email")


def handle_contact_submission(data: dict, request) -> None:
    """Save request to DB and send email notification.

    DB write always happens. Email failure is logged and swallowed so
    the user always sees a success state. In production, email is sent
    in a background thread so SMTP latency cannot block the HTTP response.
    """
    # #region agent log
    started = time.perf_counter()
    _agent_log(
        "contacts/utils.py:handle_contact_submission",
        "submission start",
        {"asyncEmail": not settings.DEBUG},
        "B",
    )
    # #endregion

    ConsultationRequest.objects.create(
        name=data["name"],
        email=data["email"],
        message=data["message"],
    )

    # #region agent log
    _agent_log(
        "contacts/utils.py:handle_contact_submission",
        "db write done",
        {"elapsedMs": int((time.perf_counter() - started) * 1000)},
        "B",
    )
    # #endregion

    recipient = SiteSettings.load().get_notification_email()
    if not recipient:
        logger.warning("Contact form email skipped: no notification recipient configured")
        # #region agent log
        _agent_log(
            "contacts/utils.py:handle_contact_submission",
            "submission end",
            {"emailSkipped": True, "elapsedMs": int((time.perf_counter() - started) * 1000)},
            "D",
        )
        # #endregion
        return

    if settings.DEBUG:
        _send_contact_notification_email(data, recipient)
    else:
        threading.Thread(
            target=_send_contact_notification_email,
            args=(data, recipient),
            daemon=True,
        ).start()

    # #region agent log
    _agent_log(
        "contacts/utils.py:handle_contact_submission",
        "submission end",
        {
            "emailQueued": not settings.DEBUG,
            "elapsedMs": int((time.perf_counter() - started) * 1000),
        },
        "E",
    )
    # #endregion
