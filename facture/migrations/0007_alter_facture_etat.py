# Generated by Django 3.2.12 on 2024-10-23 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facture', '0006_delete_categoriearticle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facture',
            name='etat',
            field=models.CharField(choices=[('impayee', 'Impayée'), ('payee', 'Payée')], default='impayee', max_length=20),
        ),
    ]
