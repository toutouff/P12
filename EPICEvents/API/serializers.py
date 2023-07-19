import sys

from rest_framework.relations import RelatedField
from rest_framework.serializers import ModelSerializer,StringRelatedField,SlugRelatedField
from CRM.models import Client,Contract,Event



class EventSerializer(ModelSerializer):
    client = StringRelatedField(many=False,read_only=True)
    supportContact = StringRelatedField(many=True)
    Event_Status = SlugRelatedField(many=False,read_only=True,slug_field='status')
    class Meta:
        model = Event
        fields = ['id','Event_Status','attendees','client','date_created','e_dates','supportContact','notes']



class ContractSerializer(ModelSerializer):
    client = StringRelatedField(many=False)
    salesContact = StringRelatedField(many=False)
    event = EventSerializer(many=True,read_only=False,required=False)
    # the serializer should display event info rather than event product Key

    class Meta:
        model = Contract
        fields = ['id','client','salesContact','event','status','amount','payment_due']

    def create(self, validated_data):
        if 'event' in validated_data:
            event_data = validated_data.pop('event')

            contract = Contract.objects.create(**validated_data)
            print(contract.client,file=sys.stderr)
            for event in event_data:
                Event.objects.create(Event_Status=contract,client=contract.client, **event)
            return contract
        else:
            contract = Contract.objects.create(**validated_data)
            event = Event.objects.create(Event_Status=contract,client=contract.client,attendees=9999,e_dates=contract.payment_due)
            return contract


class ClientSerializer(ModelSerializer):
    contracts = ContractSerializer(many=True,read_only=True)
    events = EventSerializer(many=True,read_only=True)
    class Meta:
        model = Client
        fields = ['id','firstname','lastname','email','phone','mobile','companyname','dateUpdated','is_potential','SalesContact','contracts','events']




class ContractCreationSerializer(ModelSerializer):
    class Meta:
        model = Contract
        fields = ['amount']

