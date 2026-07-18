from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0002_category_and_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='image_url',
            field=models.CharField(max_length=500, blank=True, help_text="Optional, instead of uploading a file above. Either a full image URL (e.g. from Cloudinary), or a path to a file in static/assets/, e.g. /static/assets/projects/foo.jpg. If a file is uploaded above, the upload takes priority."),
        ),
    ]
