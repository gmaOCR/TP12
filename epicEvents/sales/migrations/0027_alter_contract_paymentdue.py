# Generated by Django 4.2 on 2023-05-07 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0026_alter_contract_paymentdue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='paymentDue',
            field=models.DateField(default=None, null=True),
        ),
    ]