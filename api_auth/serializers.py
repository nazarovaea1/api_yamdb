from django.conf import settings
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from .models import User


class UserSerializer(serializers.ModelSerializer):
    bio = serializers.CharField(required=False)
    role = serializers.CharField(required=False)
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    def validate_role(self, value):
        """
        Check if user's role is in ROLE_CHOICES
        """
        if value not in settings.USER_ROLES:
            raise ValidationError(
                "Only 'user' or 'moderator' or 'admin' roles are allowed"
            )
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            bio=validated_data.get('bio', ''),
            role=validated_data.get('role', 'user'),
        )

        if validated_data.get('role') == 'admin':
            user.is_staff = True
            user.is_superuser = True

        user.is_staff = False
        user.is_superuser = False

        user.save()

        return user

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'username', 'email', 'bio', 'role',
        ]


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ('email', 'username')


class MyTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()
    email = serializers.EmailField()

    def validate_confirmation_code(self, value):
        """
        Check confirmation code returned from user
        """
        email = self.initial_data.get('email', '')
        username = self.initial_data.get('username', '')

        if not email or not username:
            raise ValidationError('The email or the username is not correct')

        password = email + username
        response_code = make_password(
            password=password, salt=settings.SECRET_KEY, hasher='default'
        ).split('$')[-1]

        if response_code != value:
            raise ValidationError('The confirmation code is not correct')

        return value
