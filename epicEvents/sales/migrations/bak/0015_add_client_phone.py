# Generated by Django 4.2 on 2023-05-05 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0014_remove_client_phone_alter_client_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='phone',
            field=models.CharField(max_length=20, blank=True,null=True, default=None)
        ),
    ]