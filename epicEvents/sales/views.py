import status as status
import logging
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404
from django.utils import timezone

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .permissions import IsSaleOrReadOnly, IsOwner, IsManager
from .models import Client, Contract, Event
from .filters import ContractFilter, ClientFilter, EventFilter
from .serializers import EventSerializer, ClientSerializer, ContractSerializer, \
    ClientListSerializer, ContractListSerializer, ContractCreateSerializer, ContractUpdateSerializer, \
    EventListSerializer, EventCreateUpdateSerializer


logger = logging.getLogger(__name__)


def not_found_view(request, exception=None):
    return HttpResponseNotFound('<h1>Page not found</h1>')


class ClientFilterViewset(ModelViewSet):
    permission_classes = [IsSaleOrReadOnly]
    detail_serializer_class = ClientSerializer
    serializer_class = ClientListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ClientFilter
    queryset = Client.objects.all()

    def check_permissions(self, request):
        if self.action != 'list':
            self.permission_denied(
                request, message='This endpoint does not support this method.'
            )

    def list(self, request):
        self.check_permissions(request)
        queryset = self.filter_queryset(self.get_queryset())
        if any(value for value in request.GET.dict().values() if value):
            serializer = self.detail_serializer_class(queryset, many=True)
        else:
            serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class ClientViewSet(ModelViewSet):
    permission_classes = [IsSaleOrReadOnly]

    serializer_class = ClientListSerializer
    detail_serializer_class = ClientSerializer
    queryset = Client.objects.all()

    def get_permissions(self):
        if self.action == 'destroy':
            permission_classes = [IsManager]
        elif self.action in ['create']:
            permission_classes = [IsManager | IsSaleOrReadOnly ]
        elif self.action == 'update':
            permission_classes = [IsManager | IsOwner]
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        print('Action used:', self.action)
        if self.action == 'retrieve':
            return self.detail_serializer_class
        elif self.action == 'list':
            return self.serializer_class
        return super(ClientViewSet, self).get_serializer_class()

    def list(self, request, *args, **kwargs):
        return Response({"message": "Use '/clients/' instead of '/client/' in your request "},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def create(self, request, *args, **kwargs):
        if request.method == 'POST':
            serializer = ClientSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(sales_contact=request.user)
                return Response({"message": "Client created.", 'data': serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Invalid method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request,  *args, **kwargs):
        if request.method in ['PUT', 'PATCH']:
            client_id = kwargs.get('pk')
            client = get_object_or_404(Client, client_id=client_id)
            serializer = ClientSerializer(client, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save(dateUpdated=timezone.now().date().strftime("%Y-%m-%d"))
                serializer = self.detail_serializer_class(client)
                return Response({'message': 'The client has been updated', 'data': serializer.data},
                                status=status.HTTP_200_OK)
            return Response({"message": "Error occurs with serializer"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Invalid method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'The client has been deleted'}, status=status.HTTP_204_NO_CONTENT)


class ContractViewSet(ModelViewSet):
    permission_classes = [IsOwner]

    serializer_class = ContractListSerializer
    detail_serializer_class = ContractSerializer
    create_serializer = ContractCreateSerializer
    update_serializer = ContractUpdateSerializer

    def get_permissions(self):
        if self.action == 'destroy':
            permission_classes = [IsManager]
        elif self.action in ['create', 'update']:
            permission_classes = [IsManager | IsOwner]
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        print('Action used:', self.action)
        if self.action == 'retrieve':
            return self.detail_serializer_class
        elif self.action == 'list':
            return self.serializer_class
        elif self.action == 'create':
            return self.create_serializer
        elif self.action == 'update':
            return self.update_serializer

        return super(ContractViewSet, self).get_serializer_class()

    def get_queryset(self):
        client_id = self.kwargs.get('client_id')
        return Contract.objects.filter(client_id=client_id)

    def list(self, request,  *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset:
            return Response({"message": "No contracts found for this client."}, status=status.HTTP_204_NO_CONTENT)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request,  *args, **kwargs):
        client_id = kwargs.get('client_id')
        contract_id = kwargs.get('pk')
        try:
            queryset = self.get_queryset().filter(client__client_id=client_id, contract_id=contract_id)
            if not queryset:
                return Response({"message": "Contract not found for this client."}, status=status.HTTP_404_NOT_FOUND)
            serializer = self.get_serializer(queryset.first())
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response({"message": "Client not found."}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request,  *args, **kwargs):
        if request.method == 'POST':
            serializer = self.get_serializer_class()(data=request.data)
            serializer.is_valid(raise_exception=True)

            client_id = kwargs.get('client_id')
            print(client_id)

            client = Client.objects.get(client_id=client_id)
            contract = serializer.save(sales_contact=request.user, client=client)

            contract.paymentDue = contract.paymentDue or None
            contract.save()

            stat = serializer.validated_data.get('status')
            payment_due = serializer.validated_data.get('paymentDue')
            if stat is True and payment_due is not None:
                event = Event.objects.create(
                    client=client,
                    eventStatus='1',
                )

            serializer = self.detail_serializer_class(contract)
            logger.info("Contract created with success for test")
            return Response({'message': 'Job done.', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        else:
            logger.debug("create method on Contract serializer got an exception")
            return Response({"message": "Invalid method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        contract_id = kwargs.get('pk')
        contract = get_object_or_404(Contract, contract_id=contract_id)
        contract.amount = request.data.get('amount', contract.amount)
        contract.status = request.data.get('status', contract.status)
        contract.paymentDue = request.data.get('paymentDue', contract.paymentDue)

        serializer = ContractUpdateSerializer(contract, data=request.data, partial=True,
                                              context={'paymentDue': contract.paymentDue})
        if serializer.is_valid():
            client_id = kwargs.get('client_id')
            client = get_object_or_404(Client, client_id=client_id)
            serializer.save(sales_contact=request.user, client=client)
            contract.paymentDue = contract.paymentDue or None
            contract.save()
            pretty_data = self.detail_serializer_class(contract)
            return Response({'message': 'Job done.', 'data': pretty_data.data}, status=status.HTTP_200_OK)
        else:
            logger.debug("update method on Contract serializer got an exception")
            return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'The contract has been deleted'}, status=status.HTTP_204_NO_CONTENT)


class ContractFilterViewset(ModelViewSet):
    permission_classes = [IsOwner]
    detail_serializer_class = ContractSerializer
    serializer_class = ContractListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ContractFilter
    queryset = Contract.objects.all()

    def check_permissions(self, request):
        if self.action != 'list':
            self.permission_denied(
                request, message='This endpoint does not support this method.'
            )

    def list(self, request):
        self.check_permissions(request)
        queryset = self.filter_queryset(self.get_queryset())
        if any(value for value in request.GET.dict().values() if value):
            serializer = self.detail_serializer_class(queryset, many=True)
        else:
            serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class EventViewSet(ModelViewSet):
    permission_classes = [IsOwner]

    queryset = Event.objects.all()
    serializer_class = EventListSerializer
    detail_serializer_class = EventSerializer
    CU_serializer_class = EventCreateUpdateSerializer

    def get_permissions(self):
        if self.action == 'destroy':
            return [IsManager()]
        elif self.action == 'create':
            return [IsOwner() or IsManager()]
        elif self.action in ['update', 'partial_update']:
            return [IsOwner() or IsManager()]
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        print('Action used:', self.action)
        if self.action == 'retrieve':
            return self.detail_serializer_class
        elif self.action == 'list':
            return self.serializer_class
        elif self.action in ['create', 'update', 'partial_update']:
            return self.CU_serializer_class
        return super(EventViewSet, self).get_serializer_class()

    def list(self, request,  *args, **kwargs):
        client_id = kwargs.get('client_id')
        contract_id = kwargs.get('contract_id')
        client = get_object_or_404(Client, client_id=client_id)
        contract = get_object_or_404(Contract, pk=contract_id, client=client)

        queryset = Event.objects.filter(client=client, contract=contract)
        if not queryset.exists():
            return Response({"message": "No events found for this client and contract."},
                            status=status.HTTP_204_NO_CONTENT)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def create(self, request,  *args, **kwargs):
        if request.method == 'POST':
            client_id = kwargs.get('client_id')
            contract_id = kwargs.get('contract_id')
            client = get_object_or_404(Client, client_id=client_id)
            try:
                contract = Contract.objects.get(pk=contract_id, client=client)
                if not contract.status:
                    raise ValidationError("The specified contract does not exist or its status is False.")
            except Contract.DoesNotExist:
                raise ValidationError("Not found")
            serializer = self.get_serializer_class()(data=request.data, context={'client': client})
            serializer.is_valid(raise_exception=True)
            event = serializer.save(client=client)
            pretty_data = self.detail_serializer_class(event)
            return Response({'message': 'Event created successfully.', 'data': pretty_data.data},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Invalid method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request,  *args, **kwargs):

        if request.method == 'PUT' or request.method == 'PATCH':
            event_id = kwargs.get('pk')
            event = get_object_or_404(Event, event_id=event_id)
            serializer = self.CU_serializer_class(event, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                serializer = self.detail_serializer_class(event)
                return Response({'message': 'Event updated successfully.', 'data': serializer.data},
                                status=status.HTTP_200_OK)
        else:
            return Response({"message": "Invalid method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):

        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'The event has been deleted'}, status=status.HTTP_204_NO_CONTENT)


class EventFilterViewset(ModelViewSet):
    permission_classes = [IsOwner]
    detail_serializer_class = EventSerializer
    serializer_class = EventListSerializer
    queryset = Event.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = EventFilter

    def check_permissions(self, request):
        if self.action != 'list':
            self.permission_denied(
                request, message='This endpoint does not support this method.'
            )

    def list(self, request):
        self.check_permissions(request)
        queryset = self.filter_queryset(self.get_queryset())
        if any(value for value in request.GET.dict().values() if value):
            serializer = self.detail_serializer_class(queryset, many=True)
        else:
            serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
