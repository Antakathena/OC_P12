from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes  # pour aller avec le décorateur APIView
from rest_framework.response import Response

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
)


from . import serializers
from .models import (
    Client,
    Event,
    Contract,
)
from .serializers import (
    ClientSerializer,
    ClientListSerializer,
    EventSerializer,
    ContractSerializer,
)
from .permissions import (
    SalesTeamPermission,
    SupportTeamPermission,
    InChargeOfClientPermission,
    InChargeOfEventPermission,
)

import logging
logger = logging.getLogger("django")

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
#
# formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')
#
# file_handler = logging.FileHandler('debug.log')
# file_handler.setlevel(logging.ERROR)
# file_handler.setformatter(formatter)
#
# stream_handler = logging.StreamHandler()
# stream_handler.setFormatter(formatter)
#
# logger.addHandler(file_handler)
# logger.addHandler(stream_handler)


@api_view(['GET'])
@permission_classes([AllowAny])
def api_overview(request):
    """ Aperçu des ENDPOINTS demandés sur une vue simple."""
    # à transformer en modelView pour plus de coherence ?
    logger.info("Hello from api-overview. How is loggin going?")

    infos = {
        "Bienvenue dans l'API Epic-Event.\
            Vous être connecté en tant que": f"{request.user}",

        "inscription": "  /signup/, méthode : POST",
        "connexion": "  /login/, méthode : POST",
        "déconnexion": "  /logout/, GET",

        "récupérer la liste d'un USER (employé)": r"  /employees/, méthode : GET",
        "récupérer les détails d'un USER (employé)": r"  /employees/{id}/, méthode : GET",

        "manager, créer un USER (employé)": "  /admin-employee/, méthode : POST",

        "manager, mettre à jour un USER (employé)": r"  /admin-employee/{id}/, méthode :  PUT",
        "manager, supprimer un USER (employé)": r"  /admin-employee/{id}/, méthode : DELETE",

        "créer un CLIENT": "  /clients/, méthode : POST",
        "récupérer les détails d'un CLIENT": r"  /clients/{id}/, méthode : GET",
        "mettre à jour un CLIENT": r"  /clients/{id}/, méthode :  PUT",
        "supprimer un CLIENT": r"  /clients/{id}/, méthode : DELETE",

        "ajouter un CONTRAT pour un client": r"  /clients/{id}/contracts, méthode : POST",
        "récupérer la liste de tous les CONTRAT d'un client": r"  /projects/{id}/users, méthode : GET",
        "modifier un CONTRAT du client": r"  /projects/{id}/users, méthode : UPDATE",
        "retirer un CONTRAT d'un client": r"  /projects/{id}/users, méthode : DELETE",

        "créer un EVENT": r"  /events/, méthode : POST",
        "récupérer la liste des EVENT (par date?)": r"  /events/, méthode : GET",
        "récupérer la liste des EVENT liés à un client": r"  /clients/{id}/events, méthode : GET",
        "Mettre à jour un EVENT": r"  /events/{id}/, méthode : PUT",
        "supprimer un EVENT": r"  /events/{id}/, méthode : DELETE",
    }
    return Response(infos)


class EventViewSet(ModelViewSet):
    """Classe des évènements (modèle EVENT)
    Visible par tous les employés authentifiés
    Manipulable par les membres de l'équipe support
    Seul le support_contact peut modifier ou supprimer l'évènement dont il est responsable
    """
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, ]

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        # logger.debug('get object')
        return obj

    def get_permissions(self):
        """ gets permissions
        for get : authenticated is enough
        to post : Events are created when their contract is registered,
            so "create" should be used only if deleted by mistake
        to put : support_contact if assigned, else management to assign someone
        """
        # here is determined what action can be performed, according to authorisation:
        if self.action == 'create':
            permission_classes = [IsAuthenticated, IsAdminUser, ]

        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated, ]
        elif self.action == 'list':
            permission_classes = [IsAuthenticated, ]
        else:
            permission_classes = [IsAuthenticated, SupportTeamPermission, InChargeOfEventPermission, ]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """ gets list of clients or a specific client
        If a client_id is given, gets a specific client,
        else gets all clients if no id has been given
        """
        event_id = self.request.GET.get(id)
        if event_id is not None:
            queryset = Event.objects.filter(id=event_id)
        else:
            queryset = Event.objects.all()
            # Sur le modèle du P10, un support devrait pouvoir accéder à ses events
            # utiliser l'attribut FK support_contact de client ? comment ?
            # queryset = Projects.filter(contributor__user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        """designate creator as author of the instance"""
        serializer.save(sales_contact=self.request.user)

    def list(self, request, ):
        """used by nested urls"""
        queryset = Event.objects.all()
        serializer = EventSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """used by nested urls"""
        queryset = Event.objects.all()
        project = get_object_or_404(queryset, pk=pk)
        serializer = EventSerializer(project)
        return Response(serializer.data)


class ContractViewSet(ModelViewSet):
    """Classe des contrats (modèle CONTRACT)
    Visible par tous les employés authentifiés
    Manipulable par les membres de l'équipe commerciale
    Seul le sales_contact peut modifier ou supprimer le contrat dont il est responsable.
    La création d'un contrat devrait déclencher la création de l'évènement associé
    et envoyer une alerte à l'équipe de gestion pour attribuer un support_contact à l'évènement.
    Associe un évènement à un client.
    """
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated, ]

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def get_queryset(self):
        """ gets list of contracts or a specific contract
        If a contract_id is given, gets a specific contract,
        else gets all contracts if no id has been given
        Should also get all contracts for a specific client
        """
        user = self.request.user
        contract_id = self.request.GET.get(id)

        if contract_id is not None:
            # TODO : verifier que le queryset est correct et sert à quelque chose
            queryset = Contract.objects.filter(id=contract_id)

            contract = self.queryset.get(
                contract_id=contract_id,
                # client_id=self.kwargs['client_pk']  # retenir le pk pour les essais ou passer par last_name
            )
            return contract
        else:
            queryset = Contract.objects.all()
            # queryset = Contract.objects.filter(client_id=self.kwargs['client_pk'])
            return queryset

    def get_permissions(self):
        """ gets permissions
        Instantiates and returns the list of permissions that this view requires.
        # pour get : authenticated, pour post : + salesTeam, pour delete et put : IsInChargePermission
        """
        if self.action == 'create':
            permission_classes = [IsAuthenticated, SalesTeamPermission, ]
        elif self.action == 'list':
            permission_classes = [IsAuthenticated, ]
        else:
            permission_classes = [IsAuthenticated, SalesTeamPermission, InChargeOfClientPermission, ]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """designate creator as author of the instance"""
        serializer.save(sales_contact=self.request.user)

    def list(self, request, ):
        """used by nested urls"""
        queryset = Contract.objects.all()
        serializer = ContractSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """used by nested urls"""
        queryset = Contract.objects.all()
        project = get_object_or_404(queryset, pk=pk)
        serializer = ContractSerializer(project)
        return Response(serializer.data)

    # comment ajouter un message pour dire que event lié au contrat créé?
    # def create(self, request, *args, **kwargs):
    #     super().create(*args, **kwargs)
    #     return Response({'success': 'Evenement créé, il faut lui attribuer un support'}, status=status.HTTP_201_Created)


class AdminClientViewSet(ModelViewSet):
    """Une vue client améliorée
    pour les commerciaux qui veulent
    voir uniquement leurs clients et accéder à leurs contrats
    Penser à l'ajouter aux imports dans urls.py
    """
    # TODO : implement or delete
    pass


class ClientViewSet(ModelViewSet):
    """
    Classe des clients.
    Les utilisateurs authentifiés peuvent voir la liste des clients (GET/list_Client),
    et les détails d'un client (GET/detail_CLient),
    Les utilisateurs authentifiés et membres de la SalesTeam peuvent créer un client (POST/create_Client).
    Seul le sales_contact peut modifier ou supprimer le client (retrieve, update, destroy_Client).
    En cas de suppression d'un commercial associé, il faudrait qu'une alerte soit envoyée
    à l'équipe de gestion pour attribuer un nouveau sales_contact au client.
    """
    serializer_class = ClientSerializer
    # serializer_action_classes = {
    #     'list': serializers.ClientListSerializer,
    # }
    # ordering_fields = ("last_name", "sales_contact")
    # queryset = Client.objects.all().order_by("last_name") ds get_queryset not working as well

    permission_classes = [IsAuthenticated, ]

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def get_serializer_context(self):  # pour dire au serializer quelle est la méthode CRUD
        context = super(ClientViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        return context

    # def get_serializer_class(self):
    #     try:
    #         return self.serializer_action_classes[self.action]
    #     except (KeyError, AttributeError):
    #         return super().get_serializer_class()

    def get_permissions(self):
        """ gets permissions
        Instantiates and returns the list of permissions that this view requires.
        to get : authenticated is enough
        to post : sales-team member
        to put : sales_contact if assigned, else management to assign someone
        """
        # here is determined what action can be performed, according to authorisation:
        if self.action == 'create':
            permission_classes = [IsAuthenticated, SalesTeamPermission, ]
        elif self.action == 'list':
            permission_classes = [IsAuthenticated, ]
        else:
            permission_classes = [IsAuthenticated, SalesTeamPermission, InChargeOfClientPermission, ]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """ gets list of clients or a specific client
        If a client_id is given, gets a specific client,
        else gets all clients if no id has been given
        """
        client_id = self.request.GET.get(id)
        if client_id is not None:
            queryset = Client.objects.filter(id=client_id)
        else:
            queryset = Client.objects.all()
            # Sur le modèle du P10, un commercial devrait pouvoir accéder à ses clients
            # utiliser l'attribut FK sales_contact de client ? comment ?
            # queryset = Projects.filter(contributor__user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        """designate creator as author of the instance"""
        serializer.save(sales_contact=self.request.user)

    def list(self, request, ):
        """used by nested urls"""
        queryset = Client.objects.all()
        serializer = ClientListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """used by nested urls"""
        queryset = Client.objects.all()
        project = get_object_or_404(queryset, pk=pk)
        serializer = ClientSerializer(project)
        return Response(serializer.data)

