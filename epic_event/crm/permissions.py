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
        print(request.user.team)
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
    # TODO check that this permission is really working : update client unauthorized
    # TODO : retirer les prints
    # TODO : question : what is the upside to have the decorator before a static method?

    def has_object_permission(self, request, view, obj):
        """Est chargé de cet élément (client/contrat si sales_contact, évènement si support_contact"""
        print(f'request: {request.user}')
        print(f'view: {view}')
        print(f'obj: {obj}')
        print(f'obj: {obj.sales_contact}')

        # if isinstance(obj, Client):
        if obj.sales_contact.id == request.user.id:  # modifié
            return True
        elif request.user.is_authenticated and request.method in SAFE_METHODS:
            return True
        else:
            return False


class InChargeOfEventPermission(BasePermission):
    """Autorisation pour le responsable de cet élément : accès à delete et put"""
    message = "Seul la personne en charge peut modifier ou supprimer cet élément"
    # TODO check that this permission is really working
    # TODO : retirer les prints
    # TODO : question : what is the upside to have the decorator before a static method?

    def has_object_permission(self, request, view, obj):
        """Est chargé de cet élément (client/contrat si sales_contact, évènement si support_contact"""
        print(f'request: {request}')
        print(f'view: {view}')
        print(f'obj: {obj}')

        if obj.support_contact == request.user:
            return True
        elif request.user.is_authenticated and request.method in SAFE_METHODS:
            return True
        else:
            return False
