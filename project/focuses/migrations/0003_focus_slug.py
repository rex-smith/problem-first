# Generated by Django 5.0.3 on 2024-03-15 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('focuses', '0002_userfollows'),
    ]

    operations = [
        migrations.AddField(
            model_name='focus',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
