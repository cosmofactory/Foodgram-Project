from users.models import CustomUser
from djoser.serializers import UserSerializer


class CustomUserSerializer(UserSerializer):
    """Custom user serializer."""

    class Meta:
        fields = [
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        ]
        model = CustomUser


class CreateUserSerializer(UserSerializer):
    """Custom user create serializer."""

    class Meta:
        fields = [
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
        ]
        model = CustomUser
