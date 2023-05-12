# Generated by Django 4.2 on 2023-05-01 13:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('client_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=25)),
                ('last_name', models.CharField(max_length=25)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('company', models.CharField(blank=True, max_length=250, null=True)),
                ('dateCreated', models.DateField(auto_now_add=True)),
                ('dateUpdated', models.DateField(blank=True, null=True)),
                ('sales_contact', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sale_clients', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'client',
            },
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('contract_id', models.AutoField(primary_key=True, serialize=False)),
                ('dateCreated', models.DateField(auto_now_add=True)),
                ('dateUpdated', models.DateField(blank=True, null=True)),
                ('status', models.BooleanField(default=False)),
                ('amount', models.FloatField(blank=True)),
                ('paymentDue', models.DateField(blank=True, null=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contract_client', to='sales.client')),
                ('sales_contact', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sale_contracts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'contract',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('event_id', models.AutoField(primary_key=True, serialize=False)),
                ('dateCreated', models.DateField(auto_now_add=True)),
                ('dateUpdated', models.DateField(blank=True, null=True)),
                ('attendes', models.IntegerField(blank=True)),
                ('eventDate', models.DateField(blank=True, null=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('eventStatus', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='event_contract', to='sales.contract')),
                ('support_contact', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='support_contracts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'event',
            },
        ),
    ]
