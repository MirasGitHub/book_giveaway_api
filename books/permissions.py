from rest_framework import viewsets, permissions


class BasePermissionViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if not self.request.user.is_authenticated:
            return [permissions.IsAuthenticatedOrReadOnly()]
        return super().get_permissions()
