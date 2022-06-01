from django.urls import path, include
from rest_framework import routers
from rest_framework_nested import routers
# documentation sur les nested routers :
# https://pypi.org/project/drf-nested-routers/

from . import views
from .views import (
    ClientViewSet,
    EventViewSet,
    ContractViewSet,
    # AdminClientViewset,
)

router = routers.SimpleRouter()
router.register('clients', ClientViewSet, basename='clients')
router.register('contracts', ContractViewSet, basename='contracts')
router.register('events', EventViewSet, basename='events')

# # On créé les nested routers :
clients_router = routers.NestedSimpleRouter(router, 'clients', lookup='clients')
clients_router.register('contracts', ContractViewSet, basename='client-contracts')
#
# projects_router.register('users', ContributorViewSet, basename='project-users')
#
# issues_router = routers.NestedSimpleRouter(projects_router, 'issues', lookup='issues')
# issues_router.register('comments', CommentViewSet, basename='issue-comments')


urlpatterns = [
    path('api-overview', views.api_overview, name="api-overview"),
    # TODO: pourquoi qd j'essaie juste '' comme sur P10 on a pas api-overview mais
    #    "admin-employees": "http://127.0.0.1:8000/admin-employees/"?
    path('', include(router.urls)),
    path('', include(clients_router.urls)),
]

# Celui-ci c'est juste pour étudier le syst. et avoir un accès admin pour gérer les utilisateurs :
# router = routers.DefaultRouter()
# router.register('admin-client', AdminClientViewset, basename='admin-clients')
#
# urlpatterns += router.urls
