from rest_framework.permissions import BasePermission

from .models import Client, Event

import logging
logger = logging.getLogger("django")

SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']


class IsAdminAuthenticated(BasePermission):  # exemple du cours d'OC = IsAdminUser
    """Autorisations de superuser/Admin"""

    def has_permission(self, request, view):
        """Ne donne l’accès qu’aux utilisateurs administrateurs authentifiés"""
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)


class ManagementTeamPermission(BasePermission):
    """Autorisations specifiques à l'équipe management, comme créer un employé ou le modifier
    Vérifier que User.team == "management"
    """

    def has_object_permission(self, request, view, obj):
        return request.user.team == "management"


class SalesTeamPermission(BasePermission):
    """Autorisations specifiques à l'équipe commerciale, comme créer un client ou un contrat
    Vérifier que User.team == "sales"
    """

    def has_object_permission(self, request, view, obj):
        """"""
        if obj.sales_contact:
            if request.user.team == "sales":
                return True
            elif request.user.is_authenticated and request.method in SAFE_METHODS:
                return True
            else:
                return False
        else:
            if request.user.team == "management":
                return True
            else:
                return False


class SupportTeamPermission(BasePermission):
    """Autorisations specifiques à l'équipe support, comme modifier un évènement
    Vérifier que User.team == "support"
    """

    def has_object_permission(self, request, view, obj):
        """"""
        if obj.support:
            if request.user.team == "support":
                return True
            elif request.user.is_authenticated and request.method in SAFE_METHODS:
                return True
            else:
                return False
        else:
            if request.user.team == "management":
                return True
            else:
                return False


class InChargeOfClientPermission(BasePermission):
    """Autorisation pour le responsable de cet élément : accès à delete et put"""
    message = "Seul la personne en charge peut modifier ou supprimer cet élément"

    def has_object_permission(self, request, view, obj):
        """Est chargé de ce client/contrat si sales_contact"""
        if obj.sales_contact:  # modifié
            if obj.sales_contact.id == request.user.id:
                return True
            elif request.user.is_authenticated and request.method in SAFE_METHODS:
                return True
            else:
                return False
        else:  # pas de sales_contact attribué
            if request.user.team == "management":
                return True
            else:
                return False


class InChargeOfEventPermission(BasePermission):
    """Autorisation pour le responsable de cet élément : accès à delete et put"""
    message = "Seul la personne en charge peut modifier ou supprimer cet élément"

    def has_object_permission(self, request, view, obj):
        """Est chargé de cet évènement si support"""
        if obj.support:
            if obj.support.id == request.user.id:
                return True
            elif request.user.is_authenticated and request.method in SAFE_METHODS:
                return True
            else:
                return False
        else:  # pas de support attribué
            if request.user.team == "management":
                return True
            else:
                return False
