# Generated by Django 4.2 on 2023-05-01 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('gestion', 'Gestion'), ('vente', 'Vente'), ('support', 'Support')], error_messages={'invalid_choice': 'Le rôle choisi est invalide. Les rôles disponibles sont : %(choices)s'}, max_length=10),
        ),
    ]
