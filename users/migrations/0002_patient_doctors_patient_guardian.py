# Generated by Django 5.1.7 on 2025-03-18 06:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='doctors',
            field=models.ManyToManyField(blank=True, related_name='patients', to='users.doctor'),
        ),
        migrations.AddField(
            model_name='patient',
            name='guardian',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='patients', to='users.guardian'),
        ),
    ]
