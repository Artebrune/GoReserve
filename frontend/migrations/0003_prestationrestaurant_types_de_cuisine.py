# Generated by Django 5.0 on 2024-07-09 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0002_prestationrestaurant'),
    ]

    operations = [
        migrations.AddField(
            model_name='prestationrestaurant',
            name='types_de_cuisine',
            field=models.JSONField(blank=True, default=list),
        ),
    ]
