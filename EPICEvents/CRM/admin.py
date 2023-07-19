import datetime

from django.contrib import admin
from django.template.defaulttags import url
from django.urls import path
from django.utils.html import format_html
from django.urls import reverse

from .models import *
from .forms import *


# Register your models here.
@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ['client', 'status', 'amount', 'payment_due']


# @admin.register(SalesUser)
# class SalesUserAdmin(admin.ModelAdmin):
#    list_display = ['username', 'findLeads']
#

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    # def get_urls(self):
    #     urls = super().get_urls()
    #     custom_urls = [
    #         path(
    #             r'^(?P<client>.+)/renewed/$',
    #             self.admin_site.admin_view(self.renewed),
    #             name='client-renewed'
    #         )
    #     ]
    #     return custom_urls + urls

    # def client_actions(self,obj):
    #     return format_html(
    #         '<a class="button" href="{}">renewed</a>',reverse('admin:client-renewed',args=[obj])
    #     )
    form = ClientForm
    sortable_by = ['dateUpdated']
    list_display = ['__str__','companyname' , 'is_potential', 'dateUpdated']
    actions = ['renewed']
    list_editable = ['companyname', 'is_potential']

    @admin.action(description='lead has been send', permissions=['change'])
    def renewed(self,request,queryset):
        for client in queryset:
            client.dateUpdated = datetime.datetime.now()
            client.save()


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['client', 'date_created', 'date_updated', 'attendees', 'e_dates']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'get_group']
    actions = ['hash_password']

    @admin.action(description='hash password so new user can login')
    def hash_password(self, request, queryset):
        for obj in queryset:
            print(obj.password)
            obj.set_password(obj.password)
            obj.save()
            print(obj.password)

# admin.site.register(SalesTeam)
# admin.site.register(SupportUser)
# admin.site.register(Client)
# admin.site.register(Contract)
# admin.site.register(SalesUser)
