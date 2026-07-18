from django.db import migrations, models
import django.db.models.deletion


def migrate_categories_forward(apps, schema_editor):
    """Turn each distinct old category string into a Category row, then
    point every Project at the matching Category row instead of the text."""
    Project = apps.get_model('mysite', 'Project')
    Category = apps.get_model('mysite', 'Category')

    for project in Project.objects.all():
        old_value = project.category_old
        if not old_value:
            continue
        category, _ = Category.objects.get_or_create(name=old_value)
        project.category = category
        project.save(update_fields=['category'])


def migrate_categories_backward(apps, schema_editor):
    """Reverse: copy the Category name back into the text field."""
    Project = apps.get_model('mysite', 'Project')

    for project in Project.objects.all():
        if project.category_id:
            project.category_old = project.category.name
            project.save(update_fields=['category_old'])


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'ordering': ['name'],
            },
        ),
        # Rename the old text field out of the way so we can read it
        # during the data migration, then remove it afterwards.
        migrations.RenameField(
            model_name='project',
            old_name='category',
            new_name='category_old',
        ),
        migrations.AddField(
            model_name='project',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='projects', to='mysite.category'),
        ),
        migrations.RunPython(migrate_categories_forward, migrate_categories_backward),
        migrations.RemoveField(
            model_name='project',
            name='category_old',
        ),
        migrations.AddField(
            model_name='project',
            name='image_url',
            field=models.URLField(blank=True, help_text="Optional. Paste a direct image URL (e.g. from Cloudinary) instead of uploading a file above. If both are set, the uploaded file takes priority."),
        ),
    ]
