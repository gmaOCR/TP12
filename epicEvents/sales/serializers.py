from django.contrib.auth import get_user_model
from rest_framework import serializers, decorators
from rest_framework.exceptions import ValidationError

from .models import Client, Contract, Event

User = get_user_model()

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for key, value in data.items():
            if value is None:
                data[key] = ""
        return data


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
        fields = ['contract_id', 'client', 'status', 'dateCreated', 'dateUpdated', 'amount', 'paymentDue',
                  'sales_contact']

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
        for field_name, field in self.fields.items():
            if field.required and not data.get(field_name):
                raise serializers.ValidationError(f"{field_name} is a required field.")
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


class ContractCreateSerializer(serializers.ModelSerializer):
    client = serializers.SerializerMethodField(method_name='get_client')
    read_only_fields = ['dateCreated', 'dateUpdated']

    class Meta:
        model = Contract
        required_fields = ['amount']
        fields = ['contract_id', 'client', 'status', 'dateCreated', 'dateUpdated', 'amount', 'paymentDue',
                  'sales_contact']


class ContractUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contract
        fields = ['status', 'dateCreated', 'dateUpdated', 'amount', 'paymentDue',
                  'sales_contact']

    def update(self, instance, validated_data):
        instance.amount = validated_data.get('amount', instance.amount)
        status = validated_data.get('status', instance.status)
        payment_due = validated_data.get('paymentDue', instance.paymentDue)

        if status is False and payment_due is not None:
            raise serializers.ValidationError("Contract must be signed to have a payment date value")
        elif status and payment_due is None:
            raise serializers.ValidationError("A payment date value must be specified for a signed contract.")

        instance.status = status
        instance.paymentDue = payment_due
        instance.save()
        return instance

    def validate_paymentDue(self, payment_due):
        status = self.initial_data.get('status', self.instance.status)

        if status and payment_due is None:
            raise serializers.ValidationError("Payment due must be set if the status is signed.")

        return payment_due


class EventSerializer(serializers.ModelSerializer):
    client = serializers.StringRelatedField(source='client.client')

    class Meta:
        model = Event
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        choices = dict(Event.CHOICES)
        representation['eventStatus'] = choices.get(representation['eventStatus'])
        if representation['eventDate'] is None:
            representation['eventDate'] = ""
        return representation


class EventListSerializer(serializers.ModelSerializer):
    client = serializers.StringRelatedField(source='client.client')

    class Meta:
        model = Event
        fields = ['event_id', 'client', 'support_contact', 'eventStatus', 'eventDate']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        choices = dict(Event.CHOICES)
        representation['eventStatus'] = choices.get(representation['eventStatus'])
        if representation['eventDate'] is None:
            representation['eventDate'] = ""
        return representation


class EventCreateUpdateSerializer(serializers.ModelSerializer):

    client = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Event
        fields = ['client', 'support_contact', 'eventStatus', 'attendes', 'eventDate', 'note']
        read_only_fields = ['dateCreated', 'dateUpdated', 'client']

    def validate_support_contact(self, value):
        user = User.objects.get(pk=value)
        if user.role != 'support':
            raise ValidationError('This user is not a support user')
        return value
