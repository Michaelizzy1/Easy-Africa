from django.contrib import admin
from .models import ContactSubmission, NewsletterSubscriber, Project


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'service', 'budget', 'created_at', 'handled']
    list_filter = ['service', 'handled', 'created_at']
    search_fields = ['name', 'email', 'message']
    readonly_fields = ['created_at']


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'subscribed_at', 'is_active']
    list_filter = ['is_active']
    search_fields = ['email']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_featured', 'display_order', 'is_published']
    list_filter = ['category', 'is_featured', 'is_published']
    search_fields = ['title', 'summary']
    list_editable = ['display_order', 'is_published']
