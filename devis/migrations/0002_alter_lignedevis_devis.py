# Generated by Django 3.2.12 on 2024-11-13 22:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('devis', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lignedevis',
            name='devis',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lignes_devis', to='devis.devis'),
        ),
    ]