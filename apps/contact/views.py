import hashlib
import logging

from django.conf import settings
from django.contrib import messages
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import redirect, render

from apps.core.content import banner_context

from .forms import ContactForm

logger = logging.getLogger(__name__)


def _client_key(request):
    address = request.META.get("REMOTE_ADDR", "unknown")
    return "contact-rate:" + hashlib.sha256(address.encode()).hexdigest()


def contact(request):
    context = banner_context("contact")
    form = ContactForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        rate_key = _client_key(request)
        submissions = cache.get(rate_key, 0)
        if submissions >= settings.CONTACT_RATE_LIMIT:
            messages.error(request, "Too many messages have been submitted. Please try again later.")
            return HttpResponse("Too many requests", status=429)

        fingerprint = hashlib.sha256(
            f"{form.cleaned_data['email']}|{form.cleaned_data['subject']}|{form.cleaned_data['message']}".encode()
        ).hexdigest()
        if request.session.get("last_contact_fingerprint") == fingerprint:
            messages.info(request, "Your message has already been received.")
            return redirect("contact:contact")

        inquiry = form.save()
        cache.set(rate_key, submissions + 1, timeout=3600)
        request.session["last_contact_fingerprint"] = fingerprint
        try:
            send_mail(
                f"Website inquiry: {inquiry.subject}",
                f"From: {inquiry.full_name} <{inquiry.email}>\nPhone: {inquiry.phone or 'Not provided'}\n\n{inquiry.message}",
                settings.DEFAULT_FROM_EMAIL,
                [settings.CONTACT_NOTIFICATION_EMAIL],
                fail_silently=False,
            )
        except Exception:
            logger.exception("Contact inquiry saved but notification email failed.")
        messages.success(request, "Thank you. Your message has been received by the hub.")
        return redirect("contact:contact")

    context["form"] = form
    return render(request, "contact/contact.html", context)
