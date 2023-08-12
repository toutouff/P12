import sys

from rest_framework.relations import RelatedField
from rest_framework.serializers import ModelSerializer,StringRelatedField,SlugRelatedField
from CRM.models import Client,Contract,Event



class EventSerializer(ModelSerializer):
    """
    Event Serializer
    :param ModelSerializer: ModelSerializer
    :type ModelSerializer: ModelSerializer
    """
    class Meta:
        model = Event
        fields = ['id','Event_Status','attendees','client','date_created','e_dates','supportContact','notes']



class ContractSerializer(ModelSerializer):
    """
    Contract Serializer
    :param ModelSerializer: ModelSerializer
    :type ModelSerializer: ModelSerializer
    """
    class Meta:
        model = Contract
        fields = ['id','client','salesContact','event','status','amount','payment_due']



class ClientSerializer(ModelSerializer):
    """
    Client Serializer
    :param ModelSerializer: ModelSerializer
    :type ModelSerializer: ModelSerializer
    """
    contracts = ContractSerializer(many=True,read_only=True)
    events = EventSerializer(many=True,read_only=True)
    class Meta:
        model = Client
        fields = ['id','firstname','lastname','email','phone','mobile','companyname','dateUpdated','is_potential','salesContact','contracts','events']
