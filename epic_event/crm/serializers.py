from rest_framework import serializers
from .models import Client, Contract, Event


class ClientListSerializer(serializers.ModelSerializer):
    client_id = serializers.ReadOnlyField(source='id')
    sales_contact = serializers.ReadOnlyField(source='sales_contact.username')
    # nb : on choisit ici de donner le nom (username) du commercial plutôt que l'id

    class Meta:
        model = Client
        fields = ['client_id', 'first_name', 'last_name', 'company_name', 'sales_contact']


class ClientSerializer(serializers.ModelSerializer):
    date_created = serializers.ReadOnlyField()
    client_id = serializers.ReadOnlyField(source='id')
    status = serializers.ChoiceField(choices=Client.CHOICES)
    sales_contact = serializers.ReadOnlyField(source='sales_contact.username')
    # nb : on choisit ici de donner le nom (username) du commercial plutôt que l'id

    class Meta:
        model = Client
        fields = '__all__'


class ContractSerializer(serializers.ModelSerializer):
    contract_id = serializers.ReadOnlyField(source='id')
    # event = serializers.ReadOnlyField(source='event_id')
    # l'évent lié doit être créé en même temps que le contrat est enregistré (cf contract model)

    # Got a `TypeError` when calling `Contract.objects.create()`.
    # This may be because you have a writable field on the serializer class
    # that is not a valid argument to `Contract.objects.create()`.
    # You may need to make the field read-only,
    # or override the ContractSerializer.create() method to handle this correctly.
    class Meta:
        model = Contract
        fields = ['contract_id', 'object', 'date_signature', 'client']


class EventSerializer(serializers.ModelSerializer):
    event_id = serializers.ReadOnlyField(source='id')

    class Meta:
        model = Event
        fields = '__all__'
