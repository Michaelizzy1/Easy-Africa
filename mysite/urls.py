from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('work/', views.work, name='work'),
    path('contact/', views.contact, name='contact'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms/', views.terms, name='terms'),

    # Form submission endpoints (called via fetch() from static/js/main.js)
    path('contact/submit/', views.contact_submit, name='contact_submit'),
    path('newsletter/submit/', views.newsletter_submit, name='newsletter_submit'),
]