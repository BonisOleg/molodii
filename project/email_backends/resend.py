"""Resend HTTP API backend (Render free tier blocks outbound SMTP on port 587)."""
from __future__ import annotations

import json
import logging
import urllib.error
import urllib.request

from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.message import EmailMessage, EmailMultiAlternatives

logger = logging.getLogger(__name__)

_RESEND_API_URL = "https://api.resend.com/emails"


class ResendEmailBackend(BaseEmailBackend):
    def send_messages(self, email_messages: list[EmailMessage]) -> int:
        if not email_messages:
            return 0

        api_key = getattr(settings, "RESEND_API_KEY", "")
        if not api_key:
            if not self.fail_silently:
                raise ValueError("RESEND_API_KEY is not configured")
            logger.error("RESEND_API_KEY is not configured")
            return 0

        sent = 0
        for message in email_messages:
            try:
                self._send(message, api_key)
            except Exception:
                if not self.fail_silently:
                    raise
                logger.exception("Resend API request failed")
            else:
                sent += 1
        return sent

    def _send(self, message: EmailMessage, api_key: str) -> None:
        payload: dict[str, object] = {
            "from": message.from_email or settings.DEFAULT_FROM_EMAIL,
            "to": list(message.to),
            "subject": message.subject,
        }

        if message.cc:
            payload["cc"] = list(message.cc)
        if message.bcc:
            payload["bcc"] = list(message.bcc)
        if message.reply_to:
            payload["reply_to"] = list(message.reply_to)

        text_body, html_body = self._extract_bodies(message)
        if html_body:
            payload["html"] = html_body
        if text_body:
            payload["text"] = text_body
        elif not html_body:
            payload["text"] = ""

        request = urllib.request.Request(
            _RESEND_API_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=settings.EMAIL_TIMEOUT) as response:
                logger.info(
                    "Resend API accepted email to %s (status %s)",
                    message.to,
                    response.status,
                )
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Resend API error {exc.code}: {detail}") from exc

    @staticmethod
    def _extract_bodies(message: EmailMessage) -> tuple[str, str]:
        if isinstance(message, EmailMultiAlternatives):
            html_body = ""
            for content, mime_type in message.alternatives:
                if mime_type == "text/html":
                    html_body = content
                    break
            return message.body or "", html_body

        return message.body or "", ""
