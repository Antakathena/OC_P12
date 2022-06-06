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

    def validate(self, data):
        if self.context['request'].method == 'POST':
            if Client.objects.filter(
                first_name=data['first_name'].capitalize(),
                    last_name=data['last_name'].upper()).exists():
                error_message = 'The client is already registered.'
                raise serializers.ValidationError(error_message)
            else:
                return super().validate(data)
        else:
            return super().validate(data)


class ContractSerializer(serializers.ModelSerializer):
    contract_id = serializers.ReadOnlyField(source='id')

    class Meta:
        model = Contract
        fields = ['contract_id', 'object', 'date_signature', 'client']


class EventSerializer(serializers.ModelSerializer):
    event_id = serializers.ReadOnlyField(source='id')
    contract_id = serializers.ReadOnlyField()

    class Meta:
        model = Event
        fields = '__all__'
