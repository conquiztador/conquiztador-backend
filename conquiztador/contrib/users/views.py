from django.contrib.auth import get_user_model
from rest_framework import permissions, viewsets

from . import permissions as custom_permissions
from . import serializers

UserModel = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    http_method_names = ("get", "post", "put", "patch", "delete")

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.request.method in ("PUT", "PATCH"):
            serializer_class = serializers.UserUpdateSerializer

        return serializer_class

    def get_authenticators(self):
        if self.request.method == "POST":
            return ()

        return super().get_authenticators()

    def get_permissions(self):
        permission_classes = super().get_permissions()

        if self.request.method == "POST":
            permission_classes.append(custom_permissions.IsNotAuthenticated())
        else:
            permission_classes.append(permissions.IsAuthenticated())

            # This is usually not needed because the queryset will prohibit
            # editing other user's data but if the queryset is overrided for
            # whaterver reason this check will also prevent the modification.
            # The queryset will return 404 which is preferred while the lack
            # of permissions will cause 403 revealing the existence of the
            # user.
            permission_classes.append(custom_permissions.IsHimself())

        return permission_classes

    def get_queryset(self):
        return UserModel.objects.filter(pk=self.request.user.pk)
