import status as status
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .permissions import IsSaleOrReadOnly, IsOwner, IsManager, IsClientSalesContact
from .models import Client, Contract, Event
from .filters import ContractFilter, ClientFilter
from .serializers import EventSerializer, ClientSerializer, ContractSerializer, \
    ClientListSerializer, ContractListSerializer, ContractCreateSerializer, ContractUpdateSerializer, \
    EventListSerializer, EventCreateUpdateSerializer


class ClientFilterViewset(ModelViewSet):
    permission_classes = [IsSaleOrReadOnly]
    detail_serializer_class = ClientSerializer
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
        serializer = self.detail_serializer_class(queryset, many=True)
        return Response(serializer.data)


class ClientViewSet(ModelViewSet):
    permission_classes = [IsSaleOrReadOnly]

    serializer_class = ClientListSerializer
    detail_serializer_class = ClientSerializer
    queryset = Client.objects.all()

    def get_permissions(self):
        if self.action == 'destroy':
            permission_classes = [IsManager]
        elif self.action == 'update':
            permission_classes = [IsManager | IsSaleOrReadOnly]
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
        search_param = self.request.query_params.get('search', None)
        if search_param:
            queryset = self.filter_queryset(self.get_queryset())
            queryset = queryset.filter(last_name__icontains=search_param) | queryset.filter(
                email__icontains=search_param)
            serializer = self.detail_serializer_class(queryset, many=True)
            return Response(serializer.data)

        self.serializer_class = self.get_serializer_class()
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        if request.method == 'POST':
            serializer = ClientSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(sales_contact=request.user)
                return Response({"message": "Client created.", 'data': serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Invalid method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        if request.method in ['PUT', 'PATCH']:
            client = self.get_object()
            if 'sales_contact' in request.data and not request.user.role != "gestion":
                raise PermissionDenied("You do not have permission to modify the sales contact")
            if client.sales_contact != request.user:
                raise PermissionDenied({"message": "Only the sales contact associated with the client can update it"})
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
        if request.user.role == 'Gestion':
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({'message': 'The client has been deleted'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'message': 'This endpoint does not support this method.'}, status=status.HTTP_403_FORBIDDEN)


class ContractViewSet(ModelViewSet):
    permission_classes = [IsOwner]

    serializer_class = ContractListSerializer
    detail_serializer_class = ContractSerializer
    create_serializer = ContractCreateSerializer
    update_serializer = ContractUpdateSerializer

    def get_permissions(self):
        if self.action == 'destroy':
            permission_classes = [IsManager]
        elif self.action == 'create':
            return [IsClientSalesContact() or IsManager()]
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
        if request.method == 'POST':
            serializer = self.get_serializer_class()(data=request.data)
            serializer.is_valid(raise_exception=True)

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
            return Response({'message': 'Job done.', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Invalid method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, pk=None, client_id=None):
        contract = get_object_or_404(Contract, contract_id=pk)
        contract.amount = request.data.get('amount', contract.amount)
        contract.status = request.data.get('status', contract.status)
        contract.paymentDue = request.data.get('paymentDue', contract.paymentDue)

        serializer = ContractUpdateSerializer(contract, data=request.data, partial=True,
                                              context={'paymentDue': contract.paymentDue})
        if serializer.is_valid():
            self.check_object_permissions(request, contract)
            client = get_object_or_404(Client, client_id=client_id)
            serializer.save(sales_contact=request.user, client=client)
            contract.paymentDue = contract.paymentDue or None
            contract.save()
            pretty_data = self.detail_serializer_class(contract)
            return Response({'message': 'Job done.', 'data': pretty_data.data}, status=status.HTTP_200_OK)
        else:
            return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, client_id=None, *args, **kwargs):
        if request.user.role == 'Gestion':
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({'message': 'The contract has been deleted'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'message': 'This endpoint does not support this method.'}, status=status.HTTP_403_FORBIDDEN)


class ContractFilterViewset(ModelViewSet):
    permission_classes = [IsOwner]
    detail_serializer_class = ContractSerializer
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
        serializer = self.detail_serializer_class(queryset, many=True)
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
            return [IsClientSalesContact() or IsManager()]
        elif self.action in ['update', 'partial_update']:
            return [IsOwner() or IsClientSalesContact() or IsManager()]
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

    def list(self, request, client_id=None, contract_id=None):
        client = get_object_or_404(Client, client_id=client_id)
        contract = get_object_or_404(Contract, pk=contract_id, client=client)

        queryset = Event.objects.filter(client=client, contract=contract)
        if not queryset.exists():
            return Response({"message": "No events found for this client and contract."},
                            status=status.HTTP_204_NO_CONTENT)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, client_id=None, contract_id=None):
        if request.method == 'POST':
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

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT' or request.method == 'PATCH':
            event = self.get_object()
            serializer = self.CU_serializer_class(event, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                serializer = self.detail_serializer_class(event)
                return Response({'message': 'Event updated successfully.', 'data': serializer.data},
                                status=status.HTTP_200_OK)
        else:
            return Response({"message": "Invalid method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        if request.user.role == 'Gestion':
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({'message': 'The event has been deleted'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'message': 'You do not have permission to perform this action'},
                        status=status.HTTP_403_FORBIDDEN)


class EventFilterViewset(ModelViewSet):
    permission_classes = [IsOwner]
    detail_serializer_class = EventSerializer

    def check_permissions(self, request):
        if self.action != 'list':
            self.permission_denied(
                request, message='This endpoint does not support this method.'
            )

    def list(self, request):
        self.check_permissions(request)
        if request.method != 'GET':
            return Response({"message": "Invalid method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        queryset = Event.objects.all()
        search_param = self.request.query_params.get('search', None)
        if search_param:
            if search_param.strip():
                queryset = queryset.filter(
                    Q(client__last_name__icontains=search_param) |
                    Q(client__email__icontains=search_param) |
                    Q(eventDate__icontains=search_param)
                )
            else:
                raise ValidationError("Empty search parameter is not allowed.")
        serializer = self.detail_serializer_class(queryset, many=True)
        return Response(serializer.data)
