
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS, DjangoModelPermissions

from django.contrib.auth.models import Group
from CRM.models import Event, Client, Contract
import logging


logger = logging.getLogger(__name__)


class IsSuperUser(BasePermission):
    """
    SuperUser Permission Class
    check if user is superuser
    :param BasePermission: BasePermission
    :type BasePermission: BasePermission
    """
    def has_permission(self, request, view):
        """
        has_permission
        certifies that user is superuser
        :param self: self
        :type self: self
        :param request: request
        :type request: request
        :param view: view
        :type view: view
        :return: request.user.is_superuser
        :rtype: bool
        """
        return request.user.is_superuser


    def has_object_permission(self, request, view, obj):
        """
        has_object_permission
        certifies that user is superuser for object
        :param self: self
        :type self: self
        :param request: request
        :type request: request
        :param view: view
        :type view: view
        :param obj: obj
        :type obj: obj
        :return: request.user.is_superuser
        :rtype: bool
        """
        return request.user.is_superuser


class IsSalesPerson(BasePermission):
    """
    SalesPerson Permission Class
    check if user is in Sales group
    :param BasePermission: BasePermission
    :type BasePermission: BasePermission
    """
    def has_permission(self, request, view):
        """
        has_permission
        certifies that user is in Sales group
        :param self: self
        :type self: self
        :param request: request
        :type request: request
        :param view: view
        :type view: view
        :return: True if user is in Sales group
        :rtype: bool
        """
        if Group.objects.get(name='Sales') in request.user.get_group():
            return True
        logger.info(f'{request.user} is not in Sales group')

    def has_object_permission(self, request, view, obj):
        """
        has_object_permission
        certifies that user is in Sales group for object
        :param self: self
        :type self: self
        :param request: request
        :type request: request
        :param view: view
        :type view: view
        :param obj: obj
        :type obj: obj
        :return: True if user is in Sales group
        :rtype: bool
        """
        if request.method in SAFE_METHODS or request.method == 'POST':
            # return True if method is GET, HEAD, OPTIONS or POST
            return True
        elif type(obj) in [Client, Contract]:
            # return True if obj is Client or Contract
            # and user is salesContact of obj
            return obj.salesContact == request.user
        else:
            # return True if obj is Event and user is salesContact of obj.client
            if obj.client:
                return obj.client.salesContact == request.user
            else:
                logger.info(f'{request.user} is not in Sales group')


class IsSupportPerson(BasePermission):
    """
    SupportPerson Permission Class
    check if user is in Support group
    :param BasePermission: BasePermission
    :type BasePermission: BasePermission
    """
    def has_permission(self, request, view):
        """
        has_permission
        certifies that user is in Support group
        :param self: self
        :type self: self
        :param request: request
        :type request: request
        :param view: view
        :type view: view
        :return: True if user is in Support group
        :rtype: bool
        """
        if Group.objects.get(name='Support') in request.user.get_group():
            if type(view).__name__ == 'EventViewSet':
                # return True if user is in Support group and view is EventViewSet
                return True
            else:
                logger.info(f'{request.user} as full access only to Event')
        logger.info(f'{request.user} is not in Support group')
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        """
        has_object_permission
        certifies that user is in Support group for object
        :param self: self
        :type self: self
        :param request: request
        :type request: request
        :param view: view
        :type view: view
        :param obj: obj
        :type obj: obj
        :return: True if user is in Support group
        :rtype: bool
        """
        if request.method == 'DELETE':
            # return False if method is DELETE
            logger.info(f'{request.user} is not allowed to delete')
            return False
        elif request.method == 'POST':
            # return False if method is POST
            logger.info(f'{request.user} is not allowed to create')
            return False
        elif request.method in SAFE_METHODS:
            # return True if method is GET, HEAD, OPTIONS
            return True
        elif type(obj) == Event:
            # return True if obj is Event and user is supportContact of obj
            return obj.supportContact == request.user
        elif type(obj) == Client:
            # return True if obj is Client and user is supportContact of event of obj
            for event in Event.objects.filter(client=obj):
                if event.supportContact == request.user:
                    return True
        else:
            logger.info(f'{request.user} is not in Support group')