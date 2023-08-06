from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    has_hashed_pass = models.BooleanField(default=False)

    def get_group(self):
        return self.groups.all()


class Client(models.Model):
    firstname = models.CharField(max_length=25, null=True, blank=True)
    lastname = models.CharField(max_length=25, null=True, blank=True)
    email = models.EmailField(max_length=250, unique=True,blank=True, null=True)
    phone = models.CharField(max_length=20)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    companyname = models.CharField(max_length=250, )
    dateCreated = models.DateField(auto_now_add=True, editable=False)
    dateUpdated = models.DateTimeField(auto_now=True)
    is_potential = models.BooleanField(default=True)
    salesContact = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        if self.firstname and self.lastname:
            return f'{self.firstname[0]}. {self.lastname}'
        return f'{self.companyname}'




# class SalesUser(User):
#     class Meta:
#         verbose_name = 'SalesUser'
#
#     def findLeads(self):
#         # leads = [client for client in client_list if client.is_potential]
#         # return leads
#         pass
#
#     def convertLeads():
#         # leads = client with is potential = True
#         # estimate = temporal contract
#         # if estimate is accepted then leads become Client
#
#         pass
#
#     def followUp():
#         pass
#
#
# class SupportUser(User):
#     class Meta:
#         verbose_name = 'SupportUser'
#
#     def manageEvent():
#         pass
#
#     def updateEvent():
#         pass
#
#     def updateClient():
#         pass
#


class Contract(models.Model):
    salesContact = models.ForeignKey(User, on_delete=models.CASCADE,related_name='contracts')
    client = models.ForeignKey(Client, on_delete=models.CASCADE,related_name='contracts')
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)
    amount = models.FloatField()
    payment_due = models.DateTimeField(blank=True, null=True)

# trois
#
#
class Event(models.Model):
    client = models.ForeignKey(Client,null=True,blank=True,on_delete=models.CASCADE,related_name='events')
    date_created = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)
    supportContact = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True,related_name='events')
    Event_Status = models.ForeignKey(Contract,on_delete=models.CASCADE, null=True,related_name='event')
    attendees = models.IntegerField(blank=True, null=True)
    e_dates = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

