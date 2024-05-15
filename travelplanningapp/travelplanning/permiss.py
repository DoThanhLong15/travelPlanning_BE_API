from rest_framework import permissions


class ItemOwner(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, object):
        return request.user.is_authenticated and request.user == object.user

