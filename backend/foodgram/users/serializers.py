from djoser.serializers import (
    UserCreateSerializer as BaseUserRegistrationSerializer,)


class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = ('email', 'username', 'first_name',
                  'last_name', 'password', 'id')
