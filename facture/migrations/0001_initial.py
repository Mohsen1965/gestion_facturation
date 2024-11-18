# Generated by Django 3.2.12 on 2024-10-09 20:01

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('article', '0001_initial'),
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategorieArticle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('taux_tva', models.DecimalField(decimal_places=3, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='Facture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_facture', models.CharField(blank=True, max_length=20, unique=True)),
                ('date_facture', models.DateField(default=django.utils.timezone.now)),
                ('total_ht', models.DecimalField(decimal_places=3, max_digits=10)),
                ('total_ttc', models.DecimalField(decimal_places=3, max_digits=10)),
                ('total_remise', models.DecimalField(decimal_places=3, max_digits=10)),
                ('etat', models.CharField(choices=[('payé', 'Payé'), ('impayé', 'Impayé')], max_length=10)),
                ('total_tva', models.DecimalField(decimal_places=3, max_digits=10)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.client')),
            ],
        ),
        migrations.CreateModel(
            name='LigneFacture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantite', models.IntegerField()),
                ('prix_unitaire', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('taux_remise', models.DecimalField(decimal_places=3, default=0, max_digits=5)),
                ('montant_ht', models.DecimalField(decimal_places=3, editable=False, max_digits=10)),
                ('montant_tva', models.DecimalField(decimal_places=3, editable=False, max_digits=10)),
                ('montant_ttc', models.DecimalField(decimal_places=3, editable=False, max_digits=10)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.article')),
                ('facture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lignes', to='facture.facture')),
            ],
        ),
    ]