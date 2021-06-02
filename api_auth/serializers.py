from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    username = serializers.CharField()

    def validate_email(self, value):
        """ Checking the uniqueness of email """

        username = self.initial_data.get('username')

        if User.objects.filter(email=value).exists():
            if not User.objects.filter(username=username, email=value).exists():
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
