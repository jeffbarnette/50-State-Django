# Generated by Django 3.1.6 on 2021-02-13 06:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0002_auto_20210213_0209'),
    ]

    def generate_test_superuser(apps, schema_editor):
        from django.contrib.auth.models import User
        superuser = User.objects.create_superuser(
            username='admin',
            email='',
            password='changeme123')

        superuser.save()

    operations = [
        migrations.RunPython(generate_test_superuser),
    ]
