from djoser.serializers import (
    UserCreateSerializer as BaseUserRegistrationSerializer,)
from rest_framework.serializers import PrimaryKeyRelatedField
from users.models import User


class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    # recipes = PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta(BaseUserRegistrationSerializer.Meta):
        model = User
        fields = ('email', 'username', 'first_name',
                  'last_name', 'password', 'id')
