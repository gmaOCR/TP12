# Generated by Django 4.2 on 2023-05-05 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0006_alter_client_company_alter_client_dateupdated_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='dateCreated',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='dateUpdated',
            field=models.DateField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='dateCreated',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='dateUpdated',
            field=models.DateField(auto_now=True, null=True),
        ),
    ]
