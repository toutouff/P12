import sys

from django.shortcuts import render
from django.contrib.auth import authenticate
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework import filters, status
from CRM.models import Client, Contract, Event, User
from .serializers import ClientSerializer, ContractSerializer, EventSerializer
from CRM.permissions import IsSalesPerson,IsSupportPerson,IsSuperUser
from rest_framework.permissions import IsAuthenticated


class ClientViewSet(ModelViewSet):
    model = Client
    search_fields = ['email', 'phone', 'companyname', 'firstname', 'lastname',
                     'mobile']  # search entry will be matched against these fields
    filterset_fields = ['is_potential', 'salesContact']  # filter entry will be matched against these fields
    ordering_fields = ['dateCreated', 'dateUpdated', 'is_potential', 'id', 'salesContact__id']
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated & (IsSalesPerson | IsSupportPerson | IsSuperUser)]

    def get_queryset(self):
        return Client.objects.all()


class ContractViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated & (IsSalesPerson | IsSupportPerson)]
    model = Contract
    serializer_class = ContractSerializer
    search_field = ['client__companyname', 'client__firstname', 'client__lastname', 'client__email', 'client__phone',
                    'client__mobile']
    filterset_fields = ['status', 'payment_due']
    ordering_fields = ['dateCreated', 'dateUpdated', 'status', 'payment_due', 'id', 'client__id']
    #
    # def perform_create(self, serializer):
    #
    #     if 'Sales' in [group.name for group in self.request.user.get_group()]:
    #         salesContact = self.request.user
    #     else:
    #         salesContact = 0
    #     # TODO : add error feedback
    #
    #     if 'client_id' in self.request.data.keys():
    #         client = Client.objects.get(id=self.request.data['client_id'])
    #     else:
    #         client = 0
    #     # TODO : add error feedback
    #     if salesContact and client:
    #         serializer.save(client=client, salesContact=salesContact)

    def get_queryset(self):
        return Contract.objects.all()


class EventViewSet(ModelViewSet):
    # TODO : fix supportcontact update

    model = Event
    serializer_class = EventSerializer
    filterset_fields = ['Event_Status', 'attendees', 'supportContact__id']
    ordering_fields = ['dateCreated', 'dateUpdated', 'Event_Status', 'attendees', 'id', 'client__id']
    permission_classes = [IsAuthenticated & (IsSalesPerson | IsSupportPerson)]


    def get_queryset(self):
        return Event.objects.all()


