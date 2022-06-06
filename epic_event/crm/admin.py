from django.contrib import admin
from django.contrib.admin.models import LogEntry
from .models import Client, Contract, Event
from guardian.admin import GuardedModelAdmin
import logging

logger = logging.getLogger('django')
# logger = logging.getLogger(__name__)


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    # to have a date-based drill down navigation in the admin page
    date_hierarchy = 'action_time'

    # to filter the results by users, content types and action flags
    list_filter = [
        'user',
        'content_type',
        'action_flag'
    ]

    # when searching the user will be able to search in both object_repr and change_message
    search_fields = [
        'object_repr',
        'change_message'
    ]

    list_display = [
        'action_time',
        'user',
        'content_type',
        'action_flag',
    ]


@admin.register(Client)
class ClientAdmin(GuardedModelAdmin):
    list_display = ('first_name', 'last_name', 'company_name', 'sales_contact')  # must be a tuple
    list_filter = ('last_name', 'company_name')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.team == "support":
            return qs
        if request.user.team == "management":
            return qs
        logger.info(f"info message : {request.user} était sur la page client")
        return qs.filter(sales_contact=request.user)
        # limite la visibilité à leurs seuls clients


@admin.register(Contract)
class ContractAdmin(GuardedModelAdmin):
    list_display = ('object', 'date_signature', 'client')  # must be a tuple
    list_filter = ('object', 'date_signature', 'client')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.team == "support":
            return qs
        if request.user.team == "management":
            return qs
        logger.info(f"info message : {request.user} était sur la page contrat")
        return qs.filter(client__sales_contact=request.user)


@admin.register(Event)
class EventAdmin(GuardedModelAdmin):
    list_display = ('name', 'date', 'client', 'support')  # must be a tuple
    list_filter = ('name', 'date', 'client', 'support')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.team == "sales":
            return qs
        if request.user.team == "management":
            return qs
        logger.info(f"info message : {request.user} était sur la page évènement")
        return qs.filter(support=request.user)

# admin.site.register(Client)
# admin.site.register(Contract)
# admin.site.register(Event)
