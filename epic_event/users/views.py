from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from rest_framework import viewsets

from .models import CustomUser
from .serializers import CustomUserSerializer, RegisterUserSerializer


class AdminUserViewset(viewsets.ModelViewSet):
    """Vue réservée aux administrateurs.
    Elle permet toutes les actions du CRUD sur les users
    """
    serializer_class = RegisterUserSerializer  # au lieu de CustomUserSerializer
    queryset = users = CustomUser.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser)


class UserView(APIView):
    """ List all users """

    def get(self, *args, **kwargs):
        """Attention : les args et kwargs semblent inutiles mais ça plante sans"""
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)


class RegisterUserView(APIView):  # peut-être pas utile puisque seuls les manager peuvent le faire (dc AdminUserViewset)
    """ create a new user """
    # permission_classes = (AllowAny,)
    serializer_class = RegisterUserSerializer
    # NB : si on ne met pas ça là on a pas de formulaire adequate à remplir

    def post(self, request, *args, **kwargs):
        user = request.data
        serializer = RegisterUserSerializer(data=user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

