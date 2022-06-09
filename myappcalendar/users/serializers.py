from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]

class UserCurrentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Uses extra user model's fields in POST /users/ endpoint.
    """
    # but is not included when serializing the representation.
    password = serializers.CharField(write_only=True)
    password_repeat = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        exclude = ["role", "is_active", "last_login"]

    def validate(self, data):
        """
        Check rambler
        """
        # if '@rambler.ru' in data['email']:
        #     raise serializers.ValidationError(f"{data.get('email')} should be not in domen rambler.ru")

        if data.get('password') != data.get('password_repeat'):
            raise serializers.ValidationError(f"passwords must match!")
        # TODO Бред но непонятно как избежать, приходится удалять.
        data.pop('password_repeat')
        return data

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value