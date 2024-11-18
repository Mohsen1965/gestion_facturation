# Generated by Django 3.2.12 on 2024-10-12 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facture', '0002_remove_facture_total_remise'),
    ]

    operations = [
        migrations.AddField(
            model_name='lignefacture',
            name='montant_remise',
            field=models.DecimalField(decimal_places=3, default=0, editable=False, max_digits=10),
        ),
        migrations.AlterField(
            model_name='facture',
            name='etat',
            field=models.CharField(choices=[('impayé', 'Impayé'), ('payé', 'Payé')], max_length=20),
        ),
        migrations.AlterField(
            model_name='facture',
            name='numero_facture',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='facture',
            name='total_ht',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='facture',
            name='total_ttc',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='facture',
            name='total_tva',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=10),
        ),
    ]