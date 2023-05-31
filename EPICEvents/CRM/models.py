from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    phone = models.CharField(max_length=10)


class Client(models.Model):
    firstname = models.CharField(max_length=25, null=True, blank=True)
    lastname = models.CharField(max_length=25,null=True,blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    mobil = models.CharField(max_length=20,blank=True,null=True)
    companyname = models.CharField(max_length=250,null=True,blank=True)
    dateCreated = models.DateField(auto_now_add=True,editable=False)
    dateUpdated = models.DateTimeField(auto_now=True)
    is_potential = models.BooleanField(default=True)
    SalesContact = models.ForeignKey('SalesTeam',on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.name


class SalesTeam(User):
    class Meta:
        verbose_name = 'SalesTeam'

    def findLeads():
        # create leads(potential client)

        pass

    def convertLeads():
        # convert leads  into client
        pass

    def followUp():
        pass


class SupportTeam(User):
    class Meta:
        verbose_name = 'SupportTeam'

    def manageEvent():
        pass

    def updateEvent():
        pass

    def updateClient():
        pass


class Event(models.Model):
    client = models.ForeignKey('Client' ,on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True,editable=False,null= True)
    date_updated = models.DateTimeField(auto_now=True,null= True)
    supportContact = models.ForeignKey('SupportTeam',on_delete=models.CASCADE)
    Event_Status = 'Foreign key / int / ex : 1' # see DATA+TABLE.xlsx
    attendees = models.IntegerField(blank=True,null=True)
    e_dates = models.DateTimeField(blank=True,null=True)
    notes = models.TextField(blank=True,null=True)


class Contract(models.Model):
    salesContact = models.ForeignKey('SalesTeam',on_delete=models.CASCADE)
    client = models.ForeignKey("Client", on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True,editable=False)
    date_updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default= False)
    amount = models.FloatField()
    payment_due = models.DateTimeField(blank=True,null= True)
