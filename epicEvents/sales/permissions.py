from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
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
        if request.user.is_authenticated and request.user.role == 'vente':
            return True

        # Les utilisateurs non authentifiés ou les utilisateurs authentifiés sans le rôle 'vente' ne sont pas autorisés
        return False


class IsOwner(BasePermission):
    message = "You are not authorized to perform this action (Owner)."

    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return request.user.is_authenticated

        client_id = view.kwargs.get('client_id')
        try:
            client = Client.objects.get(client_id=client_id)
        except ObjectDoesNotExist:
            return False

        if hasattr(view, 'kwargs') and 'pk' in view.kwargs:
            try:
                event = Event.objects.get(pk=view.kwargs['pk'])
                return event.support_contact == request.user or event.client.sales_contact == request.user
            except ObjectDoesNotExist:
                pass

        return client.sales_contact == request.user

    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        if isinstance(obj, Event):
            return obj.support_contact == request.user or obj.client.sales_contact == request.user

        return obj.sales_contact == request.user and obj.client.sales_contact == request.user


class IsManager(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == 'Gestion'
        return False


class IsClientSalesContact(BasePermission):
    """
    Permission to allow only the sales_contact of a client to create an event for that client.
    """

    def has_permission(self, request, view):
        client_id = view.kwargs.get('client_id')
        if client_id is None:
            return False

        client = get_object_or_404(Client, client_id=client_id)
        return client.sales_contact == request.user


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