import logging

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from .forms import ContactForm, MemberInterestForm, NewsletterForm
from .models import Lead, NewsletterSubscriber, Service

logger = logging.getLogger(__name__)


def home(request):
    return render(
        request, "core/home.html",
        {"services": Service.objects.filter(active=True)},
    )


def about(request):
    return render(request, "core/about.html")


def services(request):
    return render(
        request, "core/services.html",
        {"services": Service.objects.filter(active=True)},
    )


def _notify_frank(subject, body):
    """Email Frank about a new lead. The lead is already saved — a mail
    failure must never lose the submission, so log and move on."""
    try:
        send_mail(
            subject, body, settings.DEFAULT_FROM_EMAIL,
            [settings.CONTACT_RECIPIENT],
        )
    except Exception:
        logger.exception("Lead saved but notification email failed")


def contact(request):
    form = ContactForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        if form.is_spam():
            return redirect("contact")
        data = form.cleaned_data
        lead = Lead.objects.create(
            name=data["name"],
            email=data["email"],
            company=data.get("company", ""),
            phone=data.get("phone", ""),
            message=data["message"],
            source=Lead.Source.CONTACT,
        )
        _notify_frank(
            f"New lead: {lead.name}" + (f" ({lead.company})" if lead.company else ""),
            (
                f"New contact form submission on badassai.ca\n\n"
                f"Name:    {lead.name}\n"
                f"Email:   {lead.email}\n"
                f"Company: {lead.company or '—'}\n"
                f"Phone:   {lead.phone or '—'}\n\n"
                f"Message:\n{lead.message}\n\n"
                f"Manage this lead: https://badassai.ca/admin/core/lead/{lead.pk}/change/"
            ),
        )
        messages.success(
            request,
            "Got it. Your message is in — Frank reads every one and will "
            "get back to you within one business day.",
        )
        return redirect("contact")
    return render(request, "core/contact.html", {"form": form})


def members(request):
    form = MemberInterestForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        if form.is_spam():
            return redirect("members")
        data = form.cleaned_data
        lead = Lead.objects.create(
            name=data["name"],
            email=data["email"],
            message="Founding-member waitlist signup.",
            source=Lead.Source.MEMBERS,
        )
        _notify_frank(
            f"New members waitlist signup: {lead.name}",
            (
                f"New founding-member waitlist signup on badassai.ca\n\n"
                f"Name:  {lead.name}\n"
                f"Email: {lead.email}\n\n"
                f"Manage this lead: https://badassai.ca/admin/core/lead/{lead.pk}/change/"
            ),
        )
        messages.success(
            request,
            "You're on the founding-member list. You'll hear from us "
            "before the doors open.",
        )
        return redirect("members")
    return render(request, "core/members.html", {"form": form})


def newsletter(request):
    form = NewsletterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        if form.is_spam():
            return redirect("newsletter")
        email = form.cleaned_data["email"]
        _, created = NewsletterSubscriber.objects.get_or_create(email=email)
        messages.success(
            request,
            "You're in. First issue lands in your inbox soon."
            if created else "You're already on the list — first issue is coming.",
        )
        return redirect("newsletter")
    return render(request, "core/newsletter.html", {"form": form})
