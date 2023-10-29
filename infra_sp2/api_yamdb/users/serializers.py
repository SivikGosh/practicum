from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import ROLE_CHOICES, User


class UserSignUpSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Имя пользователя не должно быть "me".'
            )
        return value

    class Meta:
        model = User
        fields = ('email', 'username')


class UserAdminCreateSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    role = serializers.CharField(required=False,)

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Имя пользователя не должно быть "me".'
            )
        return value

    def validate_role(self, value):
        if value in dict(ROLE_CHOICES):
            return value
        raise serializers.ValidationError(
            'Роль дожна быть определена правильно'
        )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class UserFieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class TokenSerializer(serializers.ModelSerializer):

    username = serializers.CharField(required=True)
    confirmation_code = serializers.IntegerField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
