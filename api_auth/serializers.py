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
        if value not in ['admin', 'moderator', 'user']:
            raise ValidationError(
                "Only 'user' or 'moderator' or 'admin' roles are allowed"
            )
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            bio=validated_data.get('bio', ''),
            role=validated_data.get('role', 'user'),
        )
        # create user or admin depending on role
        if validated_data.get('role') == 'admin':
            user.is_staff = True
            user.is_superuser = True
        else:
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
    email = serializers.EmailField()
    username = serializers.CharField()

    def validate_email(self, value):
        """ Checking the uniqueness of email """

        username = self.initial_data.get('username')
        email_exists = User.objects.filter(
            username=username,
            email=value
        ).exists()

        if User.objects.filter(email=value).exists():
            if not email_exists:
                raise ValidationError('This email already exists')

        return value

    def validate_username(self, value):
        """ Checking the uniqueness of username """

        email = self.initial_data.get('email')

        if User.objects.filter(username=value).exists():
            if not User.objects.filter(username=value, email=email).exists():
                raise ValidationError('This username already exists')

        return value

    class Meta:
        model = User
        fields = ['email', 'username']


class MyTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()
    email = serializers.EmailField()

    def validate_confirmation_code(self, value):
        """
        Check confirmation code returned from user
        """
        # confirmation code generation using user's email and username
        email = self.initial_data.get('email', '')
        username = self.initial_data.get('username', '')

        if email and username:
            password = email + username
            response_code = make_password(
                password=password, salt=settings.SECRET_KEY, hasher='default'
            ).split('$')[-1]

            if response_code != value:
                raise ValidationError('The confirmation code is not correct')

            return value
