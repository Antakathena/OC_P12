from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import EmployeeView, RegisterEmployeeView, AdminEmployeeViewset

app_name = 'users'  # (pour éventuellement utiliser namespace dans les urls)

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('employees/', EmployeeView.as_view()),
    path('signup/', RegisterEmployeeView.as_view()),
]

# Celui-ci c'est juste pour avoir un accès admin pour gérer les utilisateurs dans l'UI:
router = DefaultRouter()
router.register('admin-employees', AdminEmployeeViewset, basename='admin-users')

urlpatterns += router.urls
