from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from users.models import Subscribe

User = get_user_model()


class UserRegistrationSerializer(UserCreateSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('email',
                  'username',
                  'first_name',
                  'last_name',
                  'password',
                  'id',
                  'is_subscribed')

        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('username', 'email')
            )
        ]

    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError(
                'Использоваться имя me запрещено')
        if not User.objects.filter(username=data.get('username'),
                                   email=data.get('email')).exists():
            if User.objects.filter(username=data.get('username')):
                raise serializers.ValidationError(
                    'Пользователь с таким username уже существует')
            if User.objects.filter(email=data.get('email')):
                raise serializers.ValidationError(
                    'Пользователь с таким Email уже существует')
        return data

    def get_is_subscribed(self, obj):
        if (self.context.get('request')
           and not self.context['request'].user.is_anonymous):
            return Subscribe.objects.filter(
                user=self.context['request'].user,
                author=obj).exists()
        return False
