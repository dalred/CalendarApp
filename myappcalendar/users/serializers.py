from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "role"]


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Uses extra user model's fields in POST /users/ endpoint.
    """
    # but is not included when serializing the representation.
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        exclude = ["role", "is_active", "last_login"]

    def validate(self, data, ):
        """
        Check rambler
        """
        if '@rambler.ru' in data['email']:
            raise serializers.ValidationError(f"{data.get('email')} should be not in domen rambler.ru")
        return data

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user
