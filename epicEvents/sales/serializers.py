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


class ContractUpdateSerializer(ContractSerializer):
    status = serializers.BooleanField()
    paymentDue = serializers.SerializerMethodField(method_name='get_payment_due')
    read_only_fields = ['dateCreated', 'dateUpdated']

    class Meta:
        model = Contract
        fields = ['contract_id', 'client', 'status', 'dateCreated', 'dateUpdated', 'amount', 'paymentDue',
                  'sales_contact']

    def validate_status(self, status):
        payment_due = self.initial_data.get('paymentDue')
        if status and payment_due is None:
            raise serializers.ValidationError("Payment due must be set if the status is signed.")
        elif not status and payment_due:
            raise serializers.ValidationError("Payment due cannot be set without setting the status to signed.")

        return status

    def validate_paymentDue(self, paymentDue):
        status = self.initial_data.get('status')
        if status is False and paymentDue is not None:
            raise serializers.ValidationError("Status must be set to 'signed' if payment due is set.")
        elif paymentDue is None and status:
            raise serializers.ValidationError("Payment due must be set if status is 'signed'.")

        return paymentDue

    def validate(self, data):
        data['status'] = self.validate_status(data.get('status'))
        data['paymentDue'] = self.validate_paymentDue(self.context.get('paymentDue'))
        return data

    def get_payment_due(self, obj):
        payment_due = obj.paymentDue
        return payment_due if payment_due else ""

    def update(self, instance, validated_data):
        if 'status' not in validated_data:
            validated_data['status'] = instance.status
        return super().update(instance, validated_data)


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
