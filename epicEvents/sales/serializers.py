from rest_framework import serializers
from .models import Client, Contract, Event


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class ClientListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['client_id', 'first_name', 'last_name', 'sales_contact']


def get_client(obj):
    return f"{obj.client.last_name} {obj.client.first_name}"


def get_status(obj):
    return "Signé" if obj.status else "Non signé"


class ContractSerializer(serializers.ModelSerializer):
    client = serializers.SerializerMethodField(method_name='get_client')
    status = serializers.SerializerMethodField(method_name='get_status')
    paymentDue = serializers.SerializerMethodField(method_name='get_payment_due')

    class Meta:
        model = Contract
        required_fields = ['amount']
        fields = '__all__'

    @staticmethod
    def get_client(obj):
        return get_client(obj)

    @staticmethod
    def get_status(obj):
        return get_status(obj)

    @staticmethod
    def get_payment_due(obj):
        payment_due = obj.paymentDue
        if payment_due is None:
            return ''
        return payment_due

    def validate(self, data):
        for field in self.Meta.required_fields:
            if not data.get(field):
                raise serializers.ValidationError(f"{field} is a required field.")
        return data

class ContractListSerializer(serializers.ModelSerializer):
    client = serializers.SerializerMethodField(method_name='get_client')
    status = serializers.SerializerMethodField(method_name='get_status')

    class Meta:
        model = Contract
        fields = ['contract_id', 'client', 'status']

    def validate(self, attrs):
        if not attrs:
            raise serializers.ValidationError("No data provided")
        return attrs

    @staticmethod
    def get_client(obj):
        return get_client(obj)

    @staticmethod
    def get_status(obj):
        return get_status(obj)


class EventSerializer(serializers.ModelSerializer):
    client = serializers.StringRelatedField(source='client.client')
    sales_contact = serializers.StringRelatedField(source='client.sales_contact')

    class Meta:
        model = Event
        fields = '__all__'
