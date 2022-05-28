from rest_framework.permissions import BasePermission

from .models import Client, Event

SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']


class IsAdminAuthenticated(BasePermission):  # exemple du cours d'OC = IsAdminUser
    """Autorisations de superuser/Admin"""

    def has_permission(self, request, view):
        """Ne donne l’accès qu’aux utilisateurs administrateurs authentifiés"""
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)


class SalesTeamPermission(BasePermission):
    """Autorisations specifiques à l'équipe commerciale, comme créer un client ou un contrat
    Vérifier que User.team == "sales"
    """

    def has_object_permission(self, request, view, obj):
        """"""
        if request.user.team == "sales":
            return True
        elif request.user.is_authenticated and request.method in SAFE_METHODS:
            return True
        else:
            return False
        # return bool(request.user.team == "sales")


class SupportTeamPermission(BasePermission):
    """Autorisations specifiques à l'équipe support, comme modifier un évènement
    Vérifier que User.team == "support"
    """

    def has_object_permission(self, request, view, obj):
        """"""
        if request.user.team == "support":
            return True
        elif request.user.is_authenticated and request.method in SAFE_METHODS:
            return True
        else:
            return False


class InChargeOfClientPermission(BasePermission):
    """Autorisation pour le responsable de cet élément : accès à delete et put"""
    message = "Seul la personne en charge peut modifier ou supprimer cet élément"

    def has_object_permission(self, request, view, obj):
        """Est chargé de cet élément (client/contrat si sales_contact, évènement si support_contact"""
        if obj.sales_contact.id == request.user.id:  # modifié
            return True
        elif request.user.is_authenticated and request.method in SAFE_METHODS:
            return True
        else:
            return False


class InChargeOfEventPermission(BasePermission):
    """Autorisation pour le responsable de cet élément : accès à delete et put"""
    message = "Seul la personne en charge peut modifier ou supprimer cet élément"

    def has_object_permission(self, request, view, obj):
        """Est chargé de cet élément (client/contrat si sales_contact, évènement si support_contact"""
        if obj.support_contact == request.user:
            return True
        elif request.user.is_authenticated and request.method in SAFE_METHODS:
            return True
        else:
            return False
