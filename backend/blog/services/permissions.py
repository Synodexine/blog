from rest_framework.permissions import BasePermission, SAFE_METHODS


class ReadOnlyJWTPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.jwt_user and 'groups' in request.jwt_user:
            return 'Redactor' in request.jwt_user['groups']
