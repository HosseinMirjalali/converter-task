from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user model
    """

    class Meta:
        model = User
        fields = ["username", "convert_min_left", "url", "name", "password"]
        required_fields = ["username", "password"]
        read_only_fields = [
            "convert_min_left",
        ]
        extra_kwargs = {
            "password": {"write_only": True, "min_length": 5},
            "url": {"view_name": "api:user-detail", "lookup_field": "username"},
        }

    def create(self, validated_data):
        """
        Creates a user with the validated data, encrypts user's provided password
        :param validated_data: the validated data received from the user
        :return:
        """
        user = User.objects.create(**validated_data)
        user.is_active = True
        user.set_password(validated_data["password"])
        user.save()
        return user
