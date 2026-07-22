from django.conf import settings
from django.core.mail import EmailMessage
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .forms import ContactForm, NewsletterForm
from .models import Project


def robots_txt(request):
    """Serves /robots.txt — points crawlers at the sitemap and keeps the
    admin and internal form-submit endpoints out of the crawl."""
    base = f"{request.scheme}://{request.get_host()}"
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /boss/",
        "Disallow: /contact/submit/",
        "Disallow: /newsletter/submit/",
        "",
        f"Sitemap: {base}{reverse('sitemap_xml')}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def sitemap_xml(request):
    """A minimal hand-rolled sitemap covering the site's real, indexable
    pages. Static pages get a fixed lastmod; the Work page's lastmod
    tracks the most recently updated published project so it's never
    stale for long."""
    base = f"{request.scheme}://{request.get_host()}"

    latest_project = Project.objects.filter(is_published=True).order_by('-created_at').first()
    work_lastmod = latest_project.created_at.date().isoformat() if latest_project else None

    pages = [
        {"loc": reverse('home'), "priority": "1.0", "changefreq": "weekly"},
        {"loc": reverse('work'), "priority": "0.9", "changefreq": "weekly", "lastmod": work_lastmod},
        {"loc": reverse('about'), "priority": "0.7", "changefreq": "monthly"},
        {"loc": reverse('contact'), "priority": "0.7", "changefreq": "monthly"},
    ]

    xml_parts = ['<?xml version="1.0" encoding="UTF-8"?>',
                 '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for page in pages:
        xml_parts.append("  <url>")
        xml_parts.append(f"    <loc>{base}{page['loc']}</loc>")
        if page.get("lastmod"):
            xml_parts.append(f"    <lastmod>{page['lastmod']}</lastmod>")
        xml_parts.append(f"    <changefreq>{page['changefreq']}</changefreq>")
        xml_parts.append(f"    <priority>{page['priority']}</priority>")
        xml_parts.append("  </url>")
    xml_parts.append("</urlset>")

    return HttpResponse("\n".join(xml_parts), content_type="application/xml")


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
