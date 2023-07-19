import sys

from django.shortcuts import render
from django.contrib.auth import authenticate
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework import filters, status
from CRM.models import Client, Contract, Event
from .serializers import ClientSerializer, ContractSerializer, EventSerializer


class Authenticate(APIView):
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        token = Token.objects.get(user_id=user.id)
        if token:
            return Response({'status': 'auth is W.I.P', 'user': user.id, 'username': username, 'password': password,
                             'token': f'Token {token.key}'})
        else:
            token = Token.objects.create(user=user)
            return Response({'status': 'auth is W.I.P', 'user': user.id, 'username': username, 'password': password,
                             'token': token.key})


# Create your views here.
class ClientViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    model = Client
    search_fields = ['email','phone','companyname','firstname','lastname','mobile']      # search entry will be matched against these fields
    filterset_fields = ['is_potential','SalesContact']                                        # filter entry will be matched against these fields
    ordering_fields= ['dateCreated','dateUpdated','is_potential','id','SalesContact__id']
    serializer_class = ClientSerializer


    def get_queryset(self):
        groups = self.request.user.groups.all()
        for group in groups:print(group.name,file=sys.stderr)

        if self.request.user.is_superuser:
            return Client.objects.all()
        elif any(group.name == 'sales' for group in groups):
            return Client.objects.filter(SalesContact=self.request.user)
        else:
            return Client.objects.filter(events__supportContact=self.request.user) # FIXME : loop over all event and return the matching one



    @action(detail=False, methods=['get'])
    def management(self,request):
        if request.method == 'GET':
            return self.list_unasigned(request)

    def list_unasigned(self,request):
        clients = Client.objects.all()
        clients = clients.filter(SalesContact__isnull=True)
        return Response(ClientSerializer(clients,many=True).data)


    @action(detail=True, methods=['get','post'])
    def contract(self,request, pk=None):
        if request.method == 'GET':
            return self.list_contract(request, pk)
        elif request.method == 'POST':
            return self.addcontracts(request, pk)

    @action(detail=True,methods=['get','post'],url_path='event')
    def event(self,request,pk=None):
        if request.method == 'GET':
            return self.list_event(request, pk)
        elif request.method == 'POST':
            return self.add_event(request, pk)

    def list_event(self,request,pk=None):
        client = self.get_object()
        events = client.events.all()
        serializer = EventSerializer(events, many = True)
        return Response(serializer.data)

    def add_event(self,request,pk=None):
        client = self.get_object()
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            event = serializer.save(client = client)
            return Response(serializer.data)

    def list_contract(self,request, pk=None):
        client = self.get_object()
        contracts = client.contracts.all()
        serializer = ContractSerializer(contracts, many=True)
        return Response(serializer.data)

    def addcontracts(self, request, pk=None):
        client = self.get_object()
        serializer = ContractSerializer(data=request.data)
        if serializer.is_valid():
            contract = serializer.save(salesContact=request.user, client=client)
            if 'event' in request.data:
                event = EventSerializer(data=request.data["event"])
                if event.is_valid():
                    event = event.save(client=client, Event_Status=contract)
                    return Response(ContractSerializer(instance=contract).data)
                return Response(serializer.errors)
            return Response(ContractSerializer(contract).data)
        else:
            return Response(serializer.errors)

        # Todo : add support for searching and filterring
        # Todo : add support for pagination
        # todo : add getqueryset method

    @action(detail=True, methods=['get','put'],url_path='contract/(?P<contract_id>[^/.]+)')
    def contract_detail(self,request,pk=None,contract_id=None):
        if request.method == 'GET':
            return self.contract_detail_get(request,pk,contract_id)
        elif request.method == 'PUT':
            return self.contract_detail_put(request,pk,contract_id)

    def contract_detail_get(self,request,pk=None,contract_id=None):
        client = self.get_object()
        contract = client.contracts.get(id=contract_id)
        serializer = ContractSerializer(contract)
        return Response(serializer.data)

    def contract_detail_put(self,request,pk=None,contract_id=None):
        client = self.get_object()
        contract = client.contracts.get(id=contract_id)
        serializer = ContractSerializer(contract,data=request.data)
        print(serializer.initial_data,file=sys.stderr)
        if serializer.is_valid():
            print(serializer.validated_data,file=sys.stderr)
            serializer.update(instance=contract,validated_data=serializer.validated_data)
            return Response(serializer.data)

    @action(detail=True, methods=['get','put'],url_path='event/(?P<event_id>[^/.]+)')
    def event_detail(self,request,pk=None,event_id=None):
        if request.method == 'GET':
            return self.event_detail_get(request,pk,event_id)
        elif request.method in ['PUT','PATCH']:
            return self.event_update(request,pk,event_id)
        elif request.method == 'DELETE':
            return self.event_delete(request,pk,event_id)

    def event_detail_get(self,request,pk=None,event_id=None):
        client = self.get_object()
        event = Event.objects.get(id=event_id)
        print(event,file=sys.stderr)
        return Response(EventSerializer(instance=event).data)

    def event_update(self,request,pk=None,event_id=None):
        client = self.get_object()
        event = client.events.get(id=event_id)
        serializer = EventSerializer(event,data=request.data)
        if serializer.is_valid():
            serializer.update(instance=event,validated_data=serializer.validated_data)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def event_delete(self,request,pk=None,event_id=None):
        client = self.get_object()
        event = client.events.get(id=event_id)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ContractViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    model = Contract
    serializer_class = ContractSerializer
    search_field = ['client__companyname','client__firstname','client__lastname','client__email','client__phone','client__mobile']
    filterset_fields = ['status','payment_due']
    ordering_fields = ['dateCreated','dateUpdated','status','payment_due','id','client__id']

    def perform_create(self, serializer):

        # add event here

        client = Client.objects.filter(id=self.request.data['client']).first()
        print(client)
        return serializer.save(salesContact=self.request.user,client=client)

    def get_queryset(self):

        # Todo : add support for searching and filterring
        user = self.request.user
        return Contract.objects.filter(salesContact=user)

    @action(detail=True, methods=['get'])
    def event(self,request, pk=None):
        if request.method == 'GET':
            return self.list_event(request, pk)


    def list_event(self,request, pk=None):
        #  Can only be one event per contract
        contract = self.get_object()
        events = contract.event.all()
        serializer = EventSerializer(events,many=True)
        return Response(serializer.data)


class EventViewSet(ModelViewSet):
    permission_Classes = [IsAuthenticated]
    model = Event
    serializer_class = EventSerializer
    filterset_fields = ['Event_Status','attendees','supportContact__id']
    ordering_fields = ['dateCreated','dateUpdated','Event_Status','attendees','id','client__id']

    def perform_create(self, serializer):
        client = Client.objects.filter(id=self.request.data['client']).first()
        serializer.save(client=client)

    def get_queryset(self):
        user = self.request.user
        query_set = Event.objects.filter(supportContact=user)
        if not len(query_set):
            query_set = Event.objects.filter(Event_Status__salesContact=user)
            if len(query_set):
                return query_set
        return query_set







# TODO : add support to adding events to contracts Done trough serializer but not tested
# TODO : insure that you can add contract to event
