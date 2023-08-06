
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS, DjangoModelPermissions

from django.contrib.auth.models import Group
from CRM.models import Event, Client, Contract


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        print(request.user.is_superuser)
        return request.user.is_superuser


    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser


class IsSalesPerson(BasePermission):
    def has_permission(self, request, view):
        print('IsSalesPerson has permission'),print(Group.objects.all()),print(request.user.get_group()), \
            print(Group.objects.get(name='Sales') in request.user.get_group())
        if Group.objects.get(name='Sales') in request.user.get_group():
            print('has permission = True')
            return True

    def has_object_permission(self, request, view, obj):
        print('IsSalesPerson has object permission')
        if request.method in SAFE_METHODS or request.method == 'POST':
            print('Safemethod or creation')
            return True
        elif type(obj) in [Client, Contract]:
            print('object is a client or a contract and so has a salesContact attribute')
            return obj.salesContact == request.user
        else:
            print('object is Event and should has a client id')
            print(obj.client)
            if obj.client:
                return obj.client.salesContact == request.user


class IsSupportPerson(BasePermission):
    def has_permission(self, request, view):
        print('IssupportPerson permmision check')
        if Group.objects.get(name='Support') in request.user.get_group():
            print('IS support personn = true')
            return True

    def has_object_permission(self, request, view, obj):
        print('Support person object permission')
        if request.method == 'DELETE':
            return False
        elif request.method == 'POST':
            return False
        elif request.method in SAFE_METHODS:
            return True
        elif type(obj) == Event:
            print('user is support contact '),print(obj.supportContact==request.user)
            return obj.supportContact == request.user
        elif type(obj) == Client:  # fixme : support can delete Event
            for event in Event.objects.filter(client=obj):
                if event.supportContact == request.user:
                    return True

