# Generated by Django 4.2 on 2023-05-10 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0032_alter_event_attendes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='eventDate',
            field=models.DateField(blank=True, default=None, null=True),
        ),
    ]
