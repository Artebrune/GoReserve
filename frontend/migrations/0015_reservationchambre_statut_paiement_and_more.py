# Generated by Django 5.0 on 2024-08-01 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0014_reservationrestaurant'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservationchambre',
            name='statut_paiement',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='reservationrestaurant',
            name='statut_paiement',
            field=models.BooleanField(default=False),
        ),
    ]
