import random

from api.permissions import IsAuthenticatedAdmin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from api_yamdb.settings import EMAIL_HOST_USER

from .models import User
from .serializers import (TokenSerializer, UserAdminCreateSerializer,
                          UserFieldsSerializer, UserSignUpSerializer)


class UsersViewSet(viewsets.ModelViewSet):
    """Вью для создания пользователей администратором."""

    queryset = User.objects.all()
    serializer_class = UserAdminCreateSerializer
    permission_classes = (permissions.IsAuthenticated, IsAuthenticatedAdmin)
    pagination_class = PageNumberPagination
    lookup_field = 'username'

    @action(
        detail=False,
        methods=['GET', 'PATCH'],
        permission_classes=(permissions.IsAuthenticated,),
        url_path='me'
    )
    def me(self, request):
        user = User.objects.get(username=request.user.username)
        if request.method == 'GET':
            serializer = UserFieldsSerializer(user)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        elif request.method == 'PATCH':
            new_query_dict = self.request.data.copy()
            if not request.user.is_admin and not request.user.is_superuser:
                new_query_dict['role'] = request.user.role
            serializer = UserFieldsSerializer(
                user,
                data=new_query_dict,
                partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.validated_data,
                    status=status.HTTP_200_OK
                )
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request, username=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, username=username)
        serializer = UserFieldsSerializer(user)
        return Response(serializer.data)


class CreateUserView(APIView):
    """Вью для самостоятельной регистрации пользователя."""

    def post(self, request):
        serializer = UserSignUpSerializer(data=request.data)
        if serializer.is_valid():
            code = random.randint(1000, 9999)
            user = serializer.save(
                confirmation_code=code,
            )
            send_mail(
                'YAMDB API confirmation code',
                str(code),
                EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
            return Response(
                {'email': user.email, 'username': user.username},
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class GetAPIToken(APIView):
    """Вью для получения токена."""
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            fields = serializer.validated_data
            user = get_object_or_404(User, username=fields['username'])
            if fields['confirmation_code'] == user.confirmation_code:
                token = AccessToken.for_user(user)
                return Response(
                    {'token': str(token)},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'Неверный код'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(
            {'Неверные данные'},
            status=status.HTTP_400_BAD_REQUEST
        )
