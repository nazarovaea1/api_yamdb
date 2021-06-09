import logging

from smtplib import SMTPException

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import MyTokenSerializer, SignUpSerializer, UserSerializer

logging.basicConfig(
    filename='mail.log',
    filemode='a',
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s'
)


class MyTokenObtainPairView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = MyTokenSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        username = serializer.data.get('username')
        email = serializer.data.get('email')
        user, created = User.objects.get_or_create(
            username=username, email=email)
        data = self.get_tokens_for_user(user)

        return Response(data, status=status.HTTP_200_OK)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {'refresh': str(refresh), 'access': str(refresh.access_token)}


class CustomPagination(PageNumberPagination):
    page_size_query_param = 'page_size'


class ApiUserViewSet(viewsets.ModelViewSet):
    """
    List all users, or create a new user.
    Retrieve, update or delete selected user.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomPagination
    permission_classes = (IsAdminUser,)
    lookup_field = 'username'

    def partial_update(self, request, username):
        user = User.objects.get(username=username)
        role = request.data.get('role', None)

        if role is not None:
            user.is_staff = False
            user.is_superuser = False

            if role == 'admin':
                user.is_staff = True
                user.is_superuser = True

            user.save()

        serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class UserProfile(APIView):
    """
    Get and patch your profile
    """

    permission_classes = (IsAuthenticated,)
    USER_ATTR = ('username', 'email', 'role')

    def get(self, request, format=None):
        user = self.request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def patch(self, request, format=None):
        """ Do not allow to change username, email and role in profile """
        for item in request.data.keys():
            if item in self.USER_ATTR:
                raise ValidationError(
                    'Changing username, email and role is not permitted'
                )
        user = self.request.user
        serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignUpEmail(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        email = serializer.data.get('email')
        username = serializer.data.get('username')
        self.send_mail(email, username)

        return Response(
            {'info': 'Confirmation code was sent to your email'},
            status=status.HTTP_201_CREATED
        )

    def send_mail(self, email, username):
        password = email + username
        confirmation_code = make_password(
            password=password, salt=settings.SECRET_KEY, hasher='default'
        ).split('$')[-1]

        try:
            send_mail('Sign up new user',
                      f'Your confirmation code: {confirmation_code}',
                      'noreply@yatube.ru',
                      [email],
                      fail_silently=False,)
        except SMTPException as e:
            logging.error(e, exc_info=True)
            return Response(
                {'info': 'There was an error sending an email: ' + e},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception:
            logging.exception()
            return Response(
                {'info': 'Mail Sending Failed'},
                status=status.HTTP_400_BAD_REQUEST
            )
