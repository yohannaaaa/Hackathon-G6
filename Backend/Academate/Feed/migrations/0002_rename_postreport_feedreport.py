# Generated by Django 5.0.3 on 2024-04-10 10:27

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Feed', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PostReport',
            new_name='FeedReport',
        ),
    ]