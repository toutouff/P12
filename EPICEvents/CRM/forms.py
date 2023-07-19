from django import forms
from .models import *

class ClientForm(forms.ModelForm):
    firstname = forms.CharField(required= False,widget=forms.TextInput)
    lastname = forms.CharField(required=False,widget=forms.TextInput)
    email = forms.EmailField(required=True,widget=forms.EmailInput)
    phone = forms.CharField(required=True,widget=forms.TextInput)
    mobile = forms.CharField(required=False,widget=forms.TextInput)
    companyname = forms.CharField(required=True,widget=forms.TextInput)



class ContractForm(forms.ModelForm):
    amount = forms.IntegerField(required=False,widget=forms.NumberInput)
    payment_due = forms.DateField(required=False,widget=forms.DateField)
