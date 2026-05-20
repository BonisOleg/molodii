"""Template tags for two-field translations and language-aware URLs."""
from __future__ import annotations

import re

from django import template
from django.urls import reverse
from django.utils.html import urlize as django_urlize
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(takes_context=True)
def t(context, obj, field):
    """Return ``obj.<field>_<lang>`` with UA fallback when empty."""
    if obj is None:
        return ""
    lang = context.get("LANG", "uk")
    primary = getattr(obj, f"{field}_{lang}", None)
    if primary:
        return primary
    return getattr(obj, f"{field}_uk", "") or ""


@register.simple_tag(takes_context=True)
def url_for_lang(context, name, lang=None):
    """Reverse a route under the namespace for ``lang`` (defaults to current)."""
    target = lang or context.get("LANG", "uk")
    return reverse(f"{target}:{name}")


@register.filter(is_safe=True)
def urlize_new_tab(value):
    """Like |urlize but adds target="_blank" rel="noopener noreferrer" to every link."""
    urlized = django_urlize(value, nofollow=False)
    result = re.sub(
        r'<a ',
        '<a target="_blank" rel="noopener noreferrer" ',
        str(urlized),
    )
    return mark_safe(result)


@register.filter(is_safe=True)
def md_links(value):
    """Convert [text](url) to safe <a> links with target=_blank.

    Double newlines become paragraph breaks (<p>), single newlines become <br>.
    """
    from django.utils.html import escape

    def _process(segment: str) -> str:
        parts = re.split(r'(\[[^\]]*\]\(https?://[^)]+\))', segment)
        html: list[str] = []
        for part in parts:
            m = re.match(r'\[([^\]]*)\]\((https?://[^)]+)\)', part)
            if m:
                html.append(
                    f'<a href="{m.group(2)}" target="_blank" rel="noopener noreferrer">'
                    f'{escape(m.group(1))}</a>'
                )
            else:
                html.append(escape(part).replace('\n', '<br>'))
        return ''.join(html)

    text = str(value)
    if '\n\n' in text:
        paras = [p for p in re.split(r'\n{2,}', text) if p.strip()]
        return mark_safe('\n'.join(f'<p>{_process(p)}</p>' for p in paras))
    return mark_safe(_process(text))


@register.filter
def field_for_lang(obj, spec):
    """``{{ obj|field_for_lang:"title:uk" }}`` — non-tag access in conditionals."""
    if obj is None or ":" not in spec:
        return ""
    field, lang = spec.split(":", 1)
    return getattr(obj, f"{field}_{lang}", "") or getattr(obj, f"{field}_uk", "") or ""
