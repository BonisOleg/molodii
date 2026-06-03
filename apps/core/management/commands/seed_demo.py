"""Populate the database with starter content for local development."""
from __future__ import annotations

from django.core.management.base import BaseCommand

from apps.contacts.models import ContactsPage, Office, SocialLink
from apps.core.images import media_is_served
from apps.core.models import SiteSettings
from apps.pages.about_content import (
    APPROACH_IT,
    APPROACH_UK,
    EDUCATION_IT,
    EDUCATION_UK,
    approach_has_raw_url,
    education_has_raw_url,
)
from apps.pages.services_content import (
    SERVICE_TOPICS,
    SERVICES_INTRO_IT,
    SERVICES_INTRO_UK,
    SERVICES_OUTRO_IT,
    SERVICES_OUTRO_UK,
    services_items_are_stale,
)
from apps.pages.models import (
    AboutPage,
    HomePage,
    ServiceItem,
    ServicesPage,
    TherapyPage,
    TherapyStep,
)


def _clear_uploaded_image(field) -> None:
    """Drop DB media paths on PaaS: files are not served, static/img/seed is used instead."""
    if field:
        field.delete(save=False)


class Command(BaseCommand):
    help = "Seed singleton pages with demo content (UA + IT)."

    def handle(self, *args, **options):
        self._seed_site()
        self._seed_home()
        self._seed_about()
        self._seed_services()
        self._seed_therapy()
        self._seed_contacts()
        self.stdout.write(self.style.SUCCESS("Seed completed."))

    def _seed_site(self) -> None:
        s = SiteSettings.load()
        s.brand_name_uk = s.brand_name_uk or "Психолог – Молодій Тетяна"
        s.brand_name_it = s.brand_name_it or "Psicologa – Molodii Tetiana"
        s.tagline_uk = s.tagline_uk or "Підтримка для дорослих – онлайн та вживу (Мілан, Комо)"
        s.tagline_it = s.tagline_it or "Supporto per adulti – online e di persona (Milano, Como)"
        s.email = s.email or "molodiitetiana@gmail.com"
        s.phone = s.phone or "+393274470996"
        s.save()

    def _seed_home(self) -> None:
        p = HomePage.load()
        p.hero_title_uk = p.hero_title_uk or "Простір, де ви зможете краще зрозуміти себе та почати жити більш усвідомлено."
        p.hero_title_it = p.hero_title_it or "Uno spazio per conoscerti meglio e iniziare a vivere in modo più consapevole."
        p.hero_subtitle_uk = p.hero_subtitle_uk or (
            "Я психологиня, яка працює в Італії та народжена в Україні. "
            "Працюю з людьми у період кризи, змін та еміграції."
        )
        p.hero_subtitle_it = p.hero_subtitle_it or (
            "Sono psicologa, lavoro in Italia e sono nata in Ucraina. "
            "Accompagno le persone in periodi di crisi, cambiamento ed emigrazione."
        )
        p.hero_cta_uk = p.hero_cta_uk or "Записатися на знайомство"
        p.hero_cta_it = p.hero_cta_it or "Prenota una conoscenza"
        p.positioning_uk = p.positioning_uk or (
            "«Справжня подорож полягає не в пошуку нових земель, а в новому погляді.» — Марсель Пруст"
        )
        p.positioning_it = p.positioning_it or (
            "«Il vero viaggio di scoperta non consiste nel cercare nuove terre, "
            "ma nell'avere nuovi occhi.» — Marcel Proust"
        )
        if not media_is_served():
            _clear_uploaded_image(p.hero_image)
            _clear_uploaded_image(p.about_image)
        p.save()

    def _seed_about(self) -> None:
        a = AboutPage.load()
        a.title_uk = a.title_uk or "Про мене"
        a.title_it = a.title_it or "Su di me"
        a.lead_uk = a.lead_uk or (
            "Мій підхід формується не лише через професійну підготовку, але й через особистий досвід "
            "адаптації в новій країні та роботу в міжкультурному контексті."
        )
        a.lead_it = a.lead_it or (
            "Il mio modo di lavorare nasce non solo dalla formazione professionale, "
            "ma anche dall'esperienza personale di adattamento in un nuovo paese e dal lavoro in contesti interculturali."
        )
        a.body_uk = a.body_uk or (
            "У своїй практиці я працювала з:\n"
            "• людьми на різних етапах еміграції\n"
            "• ситуаціями домашнього насильства\n"
            "• онкохворими пацієнтами та їхніми сім’ями\n"
            "• парами з різним культурним і національним контекстом"
        )
        a.body_it = a.body_it or (
            "Nella mia pratica ho lavorato con:\n"
            "• persone in diversi momenti dell'emigrazione\n"
            "• situazioni di violenza domestica\n"
            "• pazienti oncologici e le loro famiglie\n"
            "• coppie con diverso contesto culturale e nazionale"
        )
        a.education_uk = a.education_uk or EDUCATION_UK
        a.education_it = a.education_it or EDUCATION_IT
        a.approach_uk = a.approach_uk or APPROACH_UK
        a.approach_it = a.approach_it or APPROACH_IT
        if education_has_raw_url(a.education_uk):
            a.education_uk = EDUCATION_UK
        if education_has_raw_url(a.education_it):
            a.education_it = EDUCATION_IT
        if approach_has_raw_url(a.approach_uk):
            a.approach_uk = APPROACH_UK
        if approach_has_raw_url(a.approach_it):
            a.approach_it = APPROACH_IT
        if not media_is_served():
            _clear_uploaded_image(a.photo)
        a.save()

    def _seed_services(self) -> None:
        s = ServicesPage.load()
        s.title_uk = s.title_uk or "З чим я працюю"
        s.title_it = s.title_it or "Con cosa lavoro"
        s.intro_uk = s.intro_uk or SERVICES_INTRO_UK
        s.intro_it = s.intro_it or SERVICES_INTRO_IT
        s.outro_uk = s.outro_uk or SERVICES_OUTRO_UK
        s.outro_it = s.outro_it or SERVICES_OUTRO_IT
        s.save()

        if services_items_are_stale(s.items.all()):
            s.intro_uk = SERVICES_INTRO_UK
            s.intro_it = SERVICES_INTRO_IT
            s.outro_uk = SERVICES_OUTRO_UK
            s.outro_it = SERVICES_OUTRO_IT
            s.save(update_fields=["intro_uk", "intro_it", "outro_uk", "outro_it"])

            s.items.all().delete()
            for i, (title_uk, title_it, desc_uk, desc_it) in enumerate(SERVICE_TOPICS):
                ServiceItem.objects.create(
                    page=s,
                    order=i,
                    title_uk=title_uk,
                    title_it=title_it,
                    description_uk=desc_uk,
                    description_it=desc_it,
                )
        elif not s.items.exists():
            for i, (title_uk, title_it, desc_uk, desc_it) in enumerate(SERVICE_TOPICS):
                ServiceItem.objects.create(
                    page=s,
                    order=i,
                    title_uk=title_uk,
                    title_it=title_it,
                    description_uk=desc_uk,
                    description_it=desc_it,
                )

    def _seed_therapy(self) -> None:
        t = TherapyPage.load()
        t.title_uk = t.title_uk or "Як проходять зустрічі"
        t.title_it = t.title_it or "Come procedono gli incontri"
        t.intro_uk = t.intro_uk or (
            "15-хвилинна безкоштовна розмова. "
            "На ній ми разом з’ясовуємо, з чим ви приходите, який напрямок роботи може бути доречним "
            "і чи підходимо ми одне одному.\n\n"
            "Також визначаємо формат: онлайн або особисто в Мілані чи Комо, "
            "та мову роботи — українську або італійську."
        )
        t.intro_it = t.intro_it or (
            "Una conversazione gratuita di 15 minuti. "
            "Insieme capiamo con cosa arrivate, quale direzione di lavoro può essere adatta e se siamo compatibili.\n\n"
            "Definiamo anche la modalità: online o di persona a Milano o Como, "
            "e la lingua di lavoro — ucraina o italiana."
        )
        t.format_online_uk = t.format_online_uk or (
            "Зустрічі у Zoom або Google Meet. Зручно, якщо ви далеко або не маєте змоги виходити з дому."
        )
        t.format_online_it = t.format_online_it or (
            "Incontri su Zoom o Google Meet. Comodo se sei lontano o non puoi uscire di casa."
        )
        t.format_offline_uk = t.format_offline_uk or (
            "Кабінет — спокійний простір без поспіху. Адреси — у блоці контактів."
        )
        t.format_offline_it = t.format_offline_it or (
            "Lo studio — uno spazio calmo, senza fretta. Indirizzi nella sezione contatti."
        )
        t.pricing_note_uk = t.pricing_note_uk or (
            "Сесія триває 50 хвилин. Регулярність — раз на тиждень. Вартість і деталі обговорюємо при знайомстві."
        )
        t.pricing_note_it = t.pricing_note_it or (
            "La sessione dura 50 minuti. Frequenza — settimanale. Tariffe e dettagli li discutiamo alla conoscenza."
        )
        if not media_is_served():
            _clear_uploaded_image(t.image)
        t.save()

        if not t.steps.exists():
            steps = [
                ("Знайомство", "Conoscenza", "Безкоштовна 20-хвилинна розмова: ваш запит і моя робота.", "Una conversazione gratuita di 20 minuti: la tua richiesta e il mio lavoro."),
                ("Контракт", "Contratto", "Узгоджуємо формат, регулярність, конфіденційність.", "Concordiamo formato, frequenza, riservatezza."),
                ("Перші сесії", "Prime sessioni", "Збираємо контекст, формуємо спільне бачення цілей.", "Raccogliamo il contesto, costruiamo una visione condivisa degli obiettivi."),
                ("Робота", "Lavoro", "Регулярні сесії — між ними буває домашня спостережлива практика.", "Sessioni regolari — tra una e l'altra, pratica osservativa."),
                ("Завершення", "Chiusura", "Підсумовуємо, що змінилося, і як підтримувати ці зміни далі.", "Facciamo il punto su cosa è cambiato e come sostenere questi cambiamenti."),
            ]
            for i, (tu, ti, bu, bi) in enumerate(steps, start=1):
                TherapyStep.objects.create(
                    page=t, order=i,
                    title_uk=tu, title_it=ti,
                    body_uk=bu, body_it=bi,
                )

    def _seed_contacts(self) -> None:
        c = ContactsPage.load()
        c.title_uk = c.title_uk or "Контакти"
        c.title_it = c.title_it or "Contatti"
        c.intro_uk = c.intro_uk or (
            "Найшвидший спосіб — лист на email або повідомлення нижче. Я відповідаю протягом 1–2 робочих днів."
        )
        c.intro_it = c.intro_it or (
            "Il modo più rapido — un'email o il modulo qui sotto. Rispondo entro 1–2 giorni lavorativi."
        )
        c.save()

        if not Office.objects.exists():
            Office.objects.create(
                order=0,
                city_uk="Мілан",
                city_it="Milano",
                address_uk="Via delle Camelie 12",
                address_it="Via delle Camelie 12",
                map_url="https://maps.google.com/?q=Via+delle+Camelie+12+Milano",
            )
            Office.objects.create(
                order=1,
                city_uk="Черноббіо (CO)",
                city_it="Cernobbio (CO)",
                address_uk="Via Vincenzo Monti 4",
                address_it="Via Vincenzo Monti 4",
                map_url="https://maps.google.com/?q=Via+Vincenzo+Monti+4+Cernobbio",
            )

        defaults = [
            (SocialLink.Platform.INSTAGRAM, "https://instagram.com/"),
            (SocialLink.Platform.LINKEDIN, "https://linkedin.com/"),
            (SocialLink.Platform.FACEBOOK, "https://facebook.com/"),
        ]
        for i, (platform, url) in enumerate(defaults):
            SocialLink.objects.get_or_create(platform=platform, defaults={"url": url, "order": i})
