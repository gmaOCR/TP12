import status as status
from django.core.exceptions import ObjectDoesNotExist, BadRequest, ValidationError
from django.utils import timezone

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .permissions import IsSaleOrReadOnly, IsOwner
from .models import Client, Contract, Event
from .serializers import EventSerializer, ClientSerializer, ContractSerializer, ClientListSerializer, ContractListSerializer


class ClientViewSet(ModelViewSet):
    permission_classes = [IsSaleOrReadOnly]

    serializer_class = ClientListSerializer
    detail_serializer_class = ClientSerializer
    queryset = Client.objects.all()

    def get_serializer_class(self):
        print('Action used:', self.action)
        if self.action == 'retrieve':
            return self.detail_serializer_class
        elif self.action == 'list':
            return self.serializer_class
        elif self.action == 'create':
            return self.serializer_class
        return super(ClientViewSet, self).get_serializer_class()

    def create(self, request, *args, **kwargs):
        phone = request.data.get('phone', '')
        company = request.data.get('company', '')
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(sales_contact=request.user, phone=phone, company=company)
            return Response({"message": "Client created."}, status=status.HTTP_201_CREATED)
        return Response({"message": "Error occurs with serializer"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        client = self.get_object()
        if client.sales_contact == request.user:
            serializer = ClientSerializer(client, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save(dateUpdated=timezone.now().date().strftime("%Y-%m-%d"))
                return Response({'message': 'The client has been updated'}, status=status.HTTP_200_OK)
            return Response({"message": "Error occurs with serializer"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Only the sales contact associated with the client can update it"},
                        status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        if request.user.role == 'gestion':
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({'message': 'The client has been deleted'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'message': 'This endpoint does not support this method.'}, status=status.HTTP_403_FORBIDDEN)


class ContractViewSet(ModelViewSet):
    permission_classes = [IsOwner, IsAuthenticated]

    serializer_class = ContractListSerializer
    detail_serializer_class = ContractSerializer

    def get_serializer_class(self):
        print('Action used:', self.action)
        if self.action == 'retrieve':
            return self.detail_serializer_class
        elif self.action == 'list':
            return self.serializer_class
        return super(ContractViewSet, self).get_serializer_class()
    def get_queryset(self):
        client_id = self.kwargs.get('client_id')
        return Contract.objects.filter(client_id=client_id)

    def list(self, request, client_id=None):
        queryset = self.get_queryset()
        if not queryset:
            return Response({"message": "No contracts found for this client."}, status=status.HTTP_204_NO_CONTENT)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, client_id=None):
        try:
            queryset = self.get_queryset().filter(client__client_id=client_id, contract_id=pk)
            if not queryset:
                return Response({"message": "Contract not found for this client."}, status=status.HTTP_404_NOT_FOUND)
            serializer = self.get_serializer(queryset.first())
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response({"message": "Client not found."}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, client_id=None):
        serializer = ContractSerializer(data=request.data)
        if serializer.is_valid():
            client = Client.objects.get(client_id=client_id)
            if client.sales_contact == request.user:
                payment_due = serializer.validated_data.get('paymentDue', None)
                stat = serializer.validated_data.get('status', False)
                if payment_due is not None and stat is False:
                    return Response({'error': 'Payment due cannot be set without setting the status to signed.'},
                                    status=status.HTTP_400_BAD_REQUEST)
                elif stat is True and payment_due is None:
                    return Response({'error': 'Payment due must be set if the status is signed.'},
                                    status=status.HTTP_400_BAD_REQUEST)
                contract = serializer.save(sales_contact=request.user, client=client)
                contract.paymentDue = contract.paymentDue or None
                contract.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'You are not authorized to create contracts for this client.'},
                                status=status.HTTP_403_FORBIDDEN)
        else:
            required_fields = list(serializer.errors.keys())
            message = f"The following fields are required: {', '.join(required_fields)}."
            return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        # Vérification des champs modifiés
        if 'paymentDue' in request.data and 'status' not in request.data:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            instance.status = True
            instance.save()
        elif 'status' in request.data and 'paymentDue' not in request.data:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            if instance.status == True:
                message = "A payment due date must be specified if status is true."
                return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)
        elif 'status' in request.data and 'paymentDue' in request.data:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            if instance.status == True and not instance.paymentDue:
                message = "A payment due date must be specified if status is true."
                return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)
            elif instance.paymentDue and not instance.status:
                instance.status = True
                instance.save()
        else:
            serializer.is_valid(raise_exception=True)
            serializer.save()

        return Response(serializer.data)


    def destroy(self, request, pk=None):
        return Response({'error': 'DELETE method is not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class EventViewSet(ModelViewSet):
    pass
