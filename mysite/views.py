from django.conf import settings
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .forms import ContactForm, NewsletterForm
from .models import Project


def home(request):
    projects = Project.objects.filter(is_published=True)[:2]
    return render(request, 'mysite/home.html', {'projects': projects})


def about(request):
    return render(request, 'mysite/about.html')


def work(request):
    projects = Project.objects.filter(is_published=True)
    return render(request, 'mysite/work.html', {'projects': projects})


def contact(request):
    return render(request, 'mysite/contact.html', {'form': ContactForm()})


def privacy_policy(request):
    return render(request, 'mysite/privacy_policy.html')


def terms(request):
    return render(request, 'mysite/terms.html')


@require_http_methods(['POST'])
def contact_submit(request):
    """
    Handles the contact form submission via fetch() from main.js.
    Returns JSON so the page can show an inline confirmation without reloading.
    """
    form = ContactForm(request.POST)
    if form.is_valid():
        submission = form.save()

        # Email the studio inbox. With EMAIL_BACKEND left as the console
        # backend (the default in settings.py), this just prints to the
        # terminal during development instead of sending a real email.
        # reply_to is set to the enquirer's address, so hitting "Reply" in
        # your inbox goes straight to them instead of back to yourself.
        try:
            email = EmailMessage(
                subject=f"New project inquiry: {submission.service}",
                body=(
                    f"Name: {submission.name}\n"
                    f"Email: {submission.email}\n"
                    f"Service: {submission.service}\n"
                    f"Budget: {submission.budget or 'Not specified'}\n\n"
                    f"{submission.message}"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.CONTACT_FORM_RECIPIENT],
                reply_to=[submission.email],
            )
            print("Backend:", settings.EMAIL_BACKEND)
            print("Host:", settings.EMAIL_HOST)
            print("User:", settings.EMAIL_HOST_USER)
            print("Recipient:", settings.CONTACT_FORM_RECIPIENT)

            sent = email.send(fail_silently=False)

            print("Sent:", sent)
        except Exception as e:
            # Don't let an email delivery failure block form submission —
            # the enquiry is already safely saved in the database either way.
            print(f"Email Error: {e}")
            # pass

        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'errors': form.errors}, status=400)


@require_http_methods(['POST'])
def newsletter_submit(request):
    """Handles the footer newsletter signup via fetch() from main.js."""
    form = NewsletterForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'errors': form.errors}, status=400)
