from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import SignUpSerializer


class SignUpEmail(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.data.get('email')
            username = serializer.data.get('username')
            self.send_mail(email, username)

            return Response(
                {'info': 'Confirmation code was sent to your email'},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_mail(self, email, username):
        password = email + username
        confirmation_code = make_password(
            password=password, salt="settings.SECRET_KEY", hasher="default"
        ).split("$")[-1]
        send_mail(
            'Sign up new user',
            f'Your confirmation code: {confirmation_code}',
            'noreply@yatube.ru',
            [email],
            fail_silently=False,
        )
