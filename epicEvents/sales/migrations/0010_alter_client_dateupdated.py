# Generated by Django 4.2 on 2023-05-05 11:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0009_alter_contract_dateupdated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='dateUpdated',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
