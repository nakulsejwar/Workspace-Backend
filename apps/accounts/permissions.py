from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsCollaborator(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.collaborators.all()


class IsViewer(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            obj.owner == request.user
            or request.user in obj.collaborators.all()
            or request.user in obj.viewers.all()
        )
