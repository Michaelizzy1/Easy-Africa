from django.db import models


class ContactSubmission(models.Model):
    """A message submitted through the contact form."""

    SERVICE_CHOICES = [
        ('Website', 'Website'),
        ('Mobile App', 'Mobile App'),
        ('Software', 'Software'),
        ('Branding', 'Branding'),
        ('IT Solutions', 'IT Solutions'),
        ('Not sure yet', 'Not sure yet'),
    ]

    BUDGET_CHOICES = [
        ('', 'Select a range'),
        ('₦30,000 - ₦100,000', '₦30,000 – ₦100,000'),
        ('₦100,000 - ₦300,000', '₦100,000 – ₦300,000'),
        ('₦300,000 - ₦1,000,000', '₦300,000 – ₦1,000,000'),
        ('₦1,000,000+', '₦1,000,000 and above'),
    ]

    name = models.CharField(max_length=150)
    email = models.EmailField()
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES, default='Not sure yet')
    budget = models.CharField(max_length=50, choices=BUDGET_CHOICES, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    handled = models.BooleanField(default=False, help_text="Mark as true once you've replied.")

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} — {self.service} ({self.created_at:%Y-%m-%d})"


class NewsletterSubscriber(models.Model):
    """An email address collected from the footer newsletter signup."""

    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-subscribed_at']

    def __str__(self):
        return self.email


class Category(models.Model):
    """A project category, e.g. Education, E-commerce, Retail.
    Manage these from the admin — add a new one any time instead of
    being limited to a fixed list."""
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Project(models.Model):
    """A case study / portfolio item shown on the Work page and homepage."""

    title = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                  null=True, blank=True,
                                  related_name='projects')
    summary = models.TextField(help_text="Short description shown on the card.")
    image = models.ImageField(upload_to='projects/', blank=True, null=True,
                               help_text="Upload an image, or leave blank and use the "
                                         "'Image URL' field below instead.")
    image_url = models.CharField(max_length=500, blank=True,
                                  help_text="Optional, instead of uploading a file above. Either a "
                                            "full image URL (e.g. from Cloudinary), or a path to a "
                                            "file in static/assets/, e.g. /static/assets/projects/foo.jpg. "
                                            "If a file is uploaded above, the upload takes priority.")
    is_featured = models.BooleanField(default=False,
                                       help_text="Featured projects display larger on the Work page.")
    display_order = models.PositiveIntegerField(default=0,
                                                  help_text="Lower numbers appear first.")
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['display_order', '-created_at']

    def __str__(self):
        return self.title

    @property
    def display_image_url(self):
        """The URL templates should use: uploaded file first, then the
        pasted image_url, then None (template falls back to placeholder)."""
        if self.image:
            return self.image.url
        if self.image_url:
            return self.image_url
        return None
