from djoser.serializers import (
    UserCreateSerializer as BaseUserRegistrationSerializer,)

from rest_framework.serializers import PrimaryKeyRelatedField, ValidationError
from rest_framework.validators import UniqueTogetherValidator

from users.models import User

from users.validators import user_regex_validator


class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    recipes = PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta(BaseUserRegistrationSerializer.Meta):
        model = User
        fields = ('email',
                  'username',
                  'first_name',
                  'last_name',
                  'password',
                  'id',
                  'recipes')

        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('name', 'email')
            ), user_regex_validator
        ]

    def validate(self, data):
        if data.get('username') == 'me':
            raise ValidationError(
                'Использоваться имя me запрещено')
        if not User.objects.filter(username=data.get('username'),
                                   email=data.get('email')).exists():
            if User.objects.filter(username=data.get('username')):
                raise ValidationError(
                    'Пользователь с таким username уже существует')
            if User.objects.filter(email=data.get('email')):
                raise ValidationError(
                    'Пользователь с таким Email уже существует')
        return data
