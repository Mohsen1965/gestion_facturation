# Generated by Django 5.1.3 on 2024-12-08 19:12

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devis', '0004_alter_devis_id_alter_lignedevis_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='devis',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
    ]
