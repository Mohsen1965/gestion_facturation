# Generated by Django 3.2.12 on 2024-10-23 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facture', '0007_alter_facture_etat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facture',
            name='etat',
            field=models.CharField(choices=[('impayee', 'Impayée'), ('payee', 'Payée')], default='impayée', max_length=20),
        ),
    ]
