from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import PermissionDenied, AuthenticationFailed
from rest_framework.permissions import BasePermission
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from .models import Client, Event, Contract


class IsSaleOrReadOnly(BasePermission):
    message = "You are not authorized to perform this action (Sale)."

    def has_permission(self, request, view):
        # Autoriser les requêtes de lecture à tout le monde
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return request.user.is_authenticated

        # Vérifier si l'utilisateur est authentifié et a le rôle 'vente'
        if request.user.is_authenticated and request.user.role in ['vente', 'Vente']:
            return True

        # Les utilisateurs non authentifiés ou les utilisateurs authentifiés sans le rôle 'vente' ne sont pas autorisés
        return False


class IsOwner(BasePermission):
    message = "You are not authorized to perform this action (Owner)."
    message2 = "Authentication credentials were not provided."

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.method in ['GET', 'HEAD', 'OPTIONS']:
                return True

            pk = view.kwargs.get('pk')
            client_id = view.kwargs.get('client_id')
            contract_id = view.kwargs.get('contract_id')

            if request.method == 'POST':
                if client_id and not contract_id:
                    if request.user != Client.objects.get(client_id=client_id).sales_contact:
                        raise PermissionDenied(detail=self.message)
                    return True

                if client_id and contract_id:
                    contract = Contract.objects.get(pk=contract_id)
                    if request.user != contract.client.sales_contact:
                        raise PermissionDenied(detail=self.message)
                return True

            if request.method == 'PUT':
                # print(view.kwargs)
                if pk and not client_id and not contract_id:
                    client = Client.objects.get(pk=pk)
                    if client.sales_contact != request.user:
                        raise PermissionDenied(detail=self.message)
                    return True

                if pk and client_id and not contract_id:
                    contract = Contract.objects.get(pk=pk)
                    if contract.client.sales_contact != request.user:
                        raise PermissionDenied(detail=self.message)
                    return True

                if pk and client_id and contract_id:
                    event = Event.objects.get(pk=pk)
                    if not (event.support_contact == request.user or event.client.sales_contact == request.user):
                        raise PermissionDenied(detail=self.message)
                    return True

        raise AuthenticationFailed(detail=self.message2)


class IsManager(BasePermission):
    message = "You are not authorized to perform this action (Manager)."

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role in ['gestion', 'Gestion']
        return False


def assign_group_permissions(apps, schema_editor):
    vente_group, _ = Group.objects.get_or_create(name='Vente')
    support_group, _ = Group.objects.get_or_create(name='Support')

    vente_content_types = [
        ContentType.objects.get_for_model(Client),
        ContentType.objects.get_for_model(Contract),
        ContentType.objects.get_for_model(Event),
    ]

    support_content_types = [
        ContentType.objects.get_for_model(Event),
    ]

    vente_permissions = Permission.objects.filter(content_type__in=vente_content_types)
    support_permissions = Permission.objects.filter(content_type__in=support_content_types)

    vente_group.permissions.set(vente_permissions)
    support_group.permissions.set(support_permissions)

    vente_group.save()
    support_group.save()
