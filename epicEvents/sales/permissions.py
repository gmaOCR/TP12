from rest_framework import permissions
from rest_framework.permissions import BasePermission


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


class IsOwner(BasePermission):
    message = "You are not authorized to perform this action."

    def has_object_permission(self, request, view, obj):
        # Si la requête est une requête en lecture seule (GET, HEAD, OPTIONS), autoriser tout le monde
        if request.method in permissions.SAFE_METHODS:
            return True

        # Si l'utilisateur est authentifié et qu'il est associé au contrat (via le champ sales_contact)
        if request.user.is_authenticated and obj.sales_contact == request.user:
            # Récupérer le client associé au contrat
            client = obj.client
            # Vérifier que le client est également associé à l'utilisateur (via le champ sales_contact)
            if client.sales_contact == request.user:
                return True

        return False
