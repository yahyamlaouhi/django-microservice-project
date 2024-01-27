from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate, get_user_model

# from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.authtoken.models import Token


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["username", "email", "password", "phone_number"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""

    email = serializers.CharField()
    password = serializers.CharField(
        style={"input_type": "password"}, trim_whitespace=False
    )

    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = Token
        read_only_fields = ["user"]

    def validate(self, attrs):
        """validate and authenticate the user"""
        email = attrs.get("email")
        password = attrs.get("password")
        print(email, password)

        user = authenticate(
            request=self.context.get("request"), username=email, password=password
        )
        if not user:
            msg = "Unable to authenticate with the provided credentials"
            raise serializers.ValidationError(msg, code="authentication")
        attrs["user"] = user
        return attrs
