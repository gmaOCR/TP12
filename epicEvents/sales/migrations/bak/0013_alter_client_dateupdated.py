# Generated by Django 4.2 on 2023-05-05 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0012_alter_client_dateupdated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='dateUpdated',
            field=models.DateField(auto_now=True, null=True),
        ),
    ]