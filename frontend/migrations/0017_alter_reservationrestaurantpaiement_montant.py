# Generated by Django 5.0 on 2024-08-01 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0016_reservationrestaurantpaiement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservationrestaurantpaiement',
            name='montant',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=10),
        ),
    ]
