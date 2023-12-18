from rest_framework import viewsets, status, decorators, permissions
from rest_framework.response import Response

from utils.mixins import MethodMatchingViewSetMixin

from authentication.models import CustomUser
from authentication.serializers import (
    CustomUserRegistrationSerializer,
    TokenSerializer,
    CustomUserRegistrationWithVerificationSerializer,
    CustomUserSerializer,
)


class CustomUserRegistrationViewSet(MethodMatchingViewSetMixin, viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()

    serializer_class = CustomUserRegistrationSerializer
    action_serializers = {
        "verification_register": CustomUserRegistrationWithVerificationSerializer,
        "verify_email": TokenSerializer,
    }

    http_method_names = ("post", "get")
    permission_classes = (permissions.AllowAny,)

    def _create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(CustomUserSerializer(instance).data, status=status.HTTP_201_CREATED)

    def create(self, request, *args, **kwargs):
        return self._create(request, *args, **kwargs)

    @decorators.action(methods=["POST"], detail=False)
    def verification_register(self, request, *args, **kwargs):
        return self._create(request, *args, **kwargs)

    @decorators.action(methods=["POST"], detail=True)
    def verify_email(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data["token"]
        try:
            user = CustomUser.objects.get(email_verification_token=token, is_verified=False)
            user.is_verified = True
            user.email_verification_token = ''
            user.save()
            return Response(data={"message": "Email verified successfully!"}, status=200)
        except CustomUser.DoesNotExist:
            return Response(data={"message": "Invalid or expired token."}, status=400)
