from django.conf import settings
from django.utils.crypto import get_random_string
from rest_framework import serializers

from authentication.models import CustomUser
from authentication.tasks import send_registration_email


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "id",
            "email",
            "is_verified",
            "first_name",
            "last_name",
        )


class CustomUserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'password',
            'email',
            'first_name',
            'last_name',
        )


class CustomUserRegistrationWithVerificationSerializer(CustomUserRegistrationSerializer):
    class Meta(CustomUserRegistrationSerializer.Meta):
        pass

    def create(self, validated_data):
        token = get_random_string(length=255)
        user = CustomUser.objects.create_user(**validated_data, email_verification_token=token, is_verified=False)
        verification_url = f"{settings.SITE_URL}/verify-email/{user.email}/{token}/"
        send_registration_email.delay(
            "Verify your email",
            f"Please click the following link to verify your email: {verification_url}",
            settings.EMAIL_HOST_USER,
            [user.email]
        )
        return user


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField()


class JWTTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()
