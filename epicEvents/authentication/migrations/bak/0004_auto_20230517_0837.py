from django.db import migrations
from django.contrib.auth.models import Group
from sales.permissions import IsSaleOrReadOnly, IsOwner, IsClientSalesContact


def assign_group_permissions():
    sale_permission = IsSaleOrReadOnly()
    owner_permission = IsOwner()
    client_sales_permission = IsClientSalesContact()

    vente_group = Group.objects.get(name='Vente')
    support_group = Group.objects.get(name='Support')

    vente_group.permissions.add(sale_permission, owner_permission, client_sales_permission)
    support_group.permissions.add(owner_permission)


class Migration(migrations.Migration):
    dependencies = [
        ('authentication', '0003_auto_20230517_0825'),
    ]

    operations = [
    ]
