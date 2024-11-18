# Generated by Django 3.2.12 on 2024-10-09 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_client', models.CharField(max_length=50, unique=True)),
                ('nom', models.CharField(max_length=100)),
                ('adresse', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('telephone', models.CharField(max_length=20)),
            ],
        ),
    ]
