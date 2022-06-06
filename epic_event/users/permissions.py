from rest_framework.permissions import BasePermission
import logging

logger = logging.getLogger('users.permissions')


class ManagementTeamPermission(BasePermission):
    """Autorisations specifiques à l'équipe management, comme créer un employé ou le modifier
    Vérifier que User.team == "management"
    """
    def has_permission(self, request, view):
        logger.info(f'user team: {request.user}')
        if request.user.team == "management":
            return True
        else:
            return False

