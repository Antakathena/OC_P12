import logging
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from rest_framework import viewsets

from .models import CustomUser
from .serializers import (
    CustomUserSerializer,
    RegisterUserSerializer,
    ChangePasswordSerializer
)


class AdminEmployeeViewset(viewsets.ModelViewSet):
    """Vue réservée aux administrateurs.
    Elle permet toutes les actions du CRUD sur les users
    """
    serializer_class = RegisterUserSerializer  # plus détaillé, au lieu de CustomUserSerializer
    queryset = users = CustomUser.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser)

class EmployeeView(APIView):
    """ List all users """

    def get(self, *args, **kwargs):
        """Attention : les args et kwargs semblent inutiles mais ça plante sans"""
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)


class ChangePasswordView(UpdateAPIView):
    """Employees should change their password for more security"""
    # NB : On évite le ModelViewSet pour éviter les problèmes de hashage du password
    serializer_class = ChangePasswordSerializer
    model = CustomUser

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response("Success.", status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


