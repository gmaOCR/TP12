# Generated by Django 4.2 on 2023-05-17 06:25

from django.db import migrations


def assign_group_permissions(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    # Création du groupe "Vente" et assignation des permissions
    group_vente, _ = Group.objects.get_or_create(name='Vente')
    permission_add_client = Permission.objects.get(codename='add_client')
    permission_change_client = Permission.objects.get(codename='change_client')
    group_vente.permissions.add(permission_add_client, permission_change_client)

    # Création du groupe "Support" et assignation des permissions
    group_support, _ = Group.objects.get_or_create(name='Support')
    permission_change_event = Permission.objects.get(codename='change_event')
    group_support.permissions.add(permission_change_event)


class Migration(migrations.Migration):
    dependencies = [
        ('authentication', '0002_alter_user_role_alter_user_username'),
    ]

    operations = [
        migrations.RunPython(assign_group_permissions),
    ]