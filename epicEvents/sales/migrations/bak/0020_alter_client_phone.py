# Generated by Django 4.2 on 2023-05-05 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0019_alter_client_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='phone',
            field=models.CharField(blank=True, default=None, max_length=20),
        ),
    ]
