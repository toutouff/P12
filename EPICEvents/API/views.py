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
    """
    Client ViewSet
    :param ModelViewSet: ModelViewSet
    :type ModelViewSet: ModelViewSet
    """
    model = Client
    search_fields = ['email', 'phone', 'companyname', 'firstname', 'lastname',
                     'mobile']  # search entry will be matched against these fields
    filterset_fields = ['is_potential', 'salesContact']  # filter entry will be matched against these fields
    ordering_fields = ['dateCreated', 'dateUpdated', 'is_potential', 'id', 'salesContact__id']
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated & (IsSalesPerson | IsSupportPerson | IsSuperUser)]

    def get_queryset(self):
        """
        get_queryset
        :param self: self
        :type self: self
        :return: Client.objects.all()
        :rtype: Client
        """
        return Client.objects.all()


class ContractViewSet(ModelViewSet):
    """
    Contract ViewSet
    :param ModelViewSet: ModelViewSet
    :type ModelViewSet: ModelViewSet
    """
    permission_classes = [IsAuthenticated & (IsSalesPerson | IsSupportPerson)]
    model = Contract
    serializer_class = ContractSerializer
    search_field = ['client__companyname', 'client__firstname', 'client__lastname', 'client__email', 'client__phone',
                    'client__mobile']
    filterset_fields = ['status', 'payment_due']
    ordering_fields = ['dateCreated', 'dateUpdated', 'status', 'payment_due', 'id', 'client__id']

    def get_queryset(self):
        """
        get_queryset
        :param self: self
        :type self: self
        :return: Contract.objects.all()
        :rtype: Contract
        """
        return Contract.objects.all()


class EventViewSet(ModelViewSet):
    """
    Event ViewSet
    :param ModelViewSet: ModelViewSet
    :type ModelViewSet: ModelViewSet
    """
    model = Event
    serializer_class = EventSerializer
    filterset_fields = ['Event_Status', 'attendees', 'supportContact__id']
    ordering_fields = ['dateCreated', 'dateUpdated', 'Event_Status', 'attendees', 'id', 'client__id']
    permission_classes = [IsAuthenticated & (IsSalesPerson | IsSupportPerson)]

    def get_queryset(self):
        """
        get_queryset
        :param self: self
        :type self: self
        :return: Event.objects.all()
        :rtype: Event
        """
        return Event.objects.all()