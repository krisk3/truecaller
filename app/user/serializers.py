"""
Define serializers for serializing and deserializing data.
"""

from django.contrib.auth import get_user_model, authenticate

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the user object.
    """

    class Meta:
        model = get_user_model()
        fields = [
            "phone",
            "password",
            "name",
            "email",
        ]
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}


class AuthTokenSerializer(serializers.Serializer):
    """
    Serializer for the user authentication token.
    """

    phone = serializers.CharField()
    password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """
        Validate and authenticate the user.
        """
        phone = attrs.get("phone")
        password = attrs.get("password")
        user = authenticate(
            request=self.context.get("request"),
            username=phone,
            password=password,
        )
        if not user:
            msg = "Unable to authenticate with provided credentials."
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs
