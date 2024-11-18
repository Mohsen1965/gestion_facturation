# Generated by Django 3.2.12 on 2024-10-09 20:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tva', '0001_initial'),
        ('categorie_article', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_article', models.CharField(max_length=50, unique=True)),
                ('nom', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('prix_unitaire', models.DecimalField(decimal_places=3, max_digits=10)),
                ('stock', models.IntegerField()),
                ('categorie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categorie_article.categoriearticle')),
                ('tva', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tva.tva')),
            ],
        ),
    ]
