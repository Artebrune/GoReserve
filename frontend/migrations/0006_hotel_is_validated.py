# Generated by Django 5.0 on 2024-07-14 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0005_chambre_proprietaire_menu_proprietaire_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='is_validated',
            field=models.BooleanField(default=False),
        ),
    ]
