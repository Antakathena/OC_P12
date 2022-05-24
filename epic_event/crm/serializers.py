from rest_framework import serializers
from .models import Client, Contract, Event


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

    class Meta:
        model = Contract
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    event_id = serializers.ReadOnlyField(source='id')

    class Meta:
        model = Event
        fields = '__all__'
