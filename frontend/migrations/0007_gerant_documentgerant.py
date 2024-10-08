# Generated by Django 5.0 on 2024-07-15 10:36

import django.db.models.deletion
import frontend.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0006_hotel_is_validated'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Gerant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('prenom', models.CharField(max_length=300)),
                ('pays', models.CharField(max_length=70)),
                ('coordonnees_tel', models.CharField(max_length=20)),
                ('adresse', models.CharField(max_length=350)),
                ('is_validated', models.BooleanField(default=False)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DocumentGerant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.FileField(blank=True, null=True, upload_to='gerant_documents/', validators=[frontend.models.validate_file_type])),
                ('gerant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='frontend.gerant')),
            ],
        ),
    ]
