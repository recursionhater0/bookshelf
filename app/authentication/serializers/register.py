from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from rest_framework import serializers

from authentication.models import CustomUser


class CustomUserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    is_verified = serializers.BooleanField(read_only=True, default=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'email', 'is_verified')


class CustomUserRegistrationWithVerificationSerializer(CustomUserRegistrationSerializer):
    class Meta(CustomUserRegistrationSerializer.Meta):
        pass

    def create(self, validated_data):
        token = get_random_string(length=255)
        user = CustomUser.objects.create_user(**validated_data, email_verification_token=token, is_verified=False)
        verification_url = f"{settings.SITE_URL}/verify-email/{user.email}/{token}/"
        # send_mail(
        #     'Verify your email',
        #     f'Please click the following link to verify your email: {verification_url}',
        #     settings.DEFAULT_FROM_EMAIL,
        #     [user.email],
        #     fail_silently=False,
        # )
        return user


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField()


class JWTTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()
