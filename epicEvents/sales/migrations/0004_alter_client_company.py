# Generated by Django 4.2 on 2023-05-15 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0003_alter_client_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='company',
            field=models.CharField(blank=True, default=None, max_length=250, null=True),
        ),
    ]
