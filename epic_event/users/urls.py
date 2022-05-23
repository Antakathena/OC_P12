from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import UserView, RegisterUserView, AdminUserViewset

app_name = 'users'  # (pour éventuellement utiliser namespace dans les urls)

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('userslist/', UserView.as_view()),
    path('signup/', RegisterUserView.as_view()),
]

# Celui-ci c'est juste pour étudier le syst. et avoir un accès admin pour gérer les utilisateurs :
router = DefaultRouter()
router.register('admin-users', AdminUserViewset, basename ='admin-users')

urlpatterns += router.urls