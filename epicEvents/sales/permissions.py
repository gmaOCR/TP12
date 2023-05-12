from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission
from .models import Client


class IsSaleOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        # Autoriser les requêtes de lecture à tout le monde
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        # Vérifier si l'utilisateur est authentifié et a le rôle 'vente'
        if request.user.is_authenticated and request.user.role == 'vente':
            return True

        # Les utilisateurs non authentifiés ou les utilisateurs authentifiés sans le rôle 'vente' ne sont pas autorisés
        return False


class IsSupport(BasePermission):
    message = "You are not authorized to perform this action (Support)."

    def has_permission(self, request, view):
        # Autoriser les requêtes de lecture à tout le monde
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        # Vérifier si l'utilisateur est authentifié et a le rôle 'support'
        if request.user.is_authenticated and request.user.role == 'support':
            return True

        # Les utilisateurs no


class IsOwner(BasePermission):
    message = "You are not authorized to perform this action (Owner)."

    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        client_id = view.kwargs.get('client_id')
        client = Client.objects.get(client_id=client_id)
        return client.sales_contact == request.user

    def has_object_permission(self, request, view, obj):
        print(obj)
        # Si la requête est une requête en lecture seule (GET, HEAD, OPTIONS), autoriser tout le monde
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        # Si l'utilisateur est authentifié et qu'il est associé au contrat (via le champ sales_contact)
        if request.user.is_authenticated and obj.sales_contact == request.user:
            # Récupérer le client associé au contrat
            client = obj.client
            # Vérifier que le client est également associé à l'utilisateur (via le champ sales_contact)
            if client.sales_contact == request.user:
                return True

        return False


class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'Gestion'


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
