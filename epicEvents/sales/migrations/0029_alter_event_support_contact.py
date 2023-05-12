# Generated by Django 4.2 on 2023-05-09 13:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sales', '0028_alter_contract_paymentdue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='support_contact',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='support_contracts', to=settings.AUTH_USER_MODEL),
        ),
    ]
