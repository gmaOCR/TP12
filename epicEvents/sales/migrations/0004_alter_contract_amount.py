# Generated by Django 4.2 on 2023-05-04 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0003_event_client_alter_client_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='amount',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
