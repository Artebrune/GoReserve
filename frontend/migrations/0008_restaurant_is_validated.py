# Generated by Django 5.0 on 2024-07-15 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0007_gerant_documentgerant'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='is_validated',
            field=models.BooleanField(default=False),
        ),
    ]
