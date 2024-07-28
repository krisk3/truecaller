"""
Define functions and classes to respond to client requests.
"""

from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from django.contrib.auth import get_user_model

from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
)


class CreateUserView(APIView):
    """
    Create a new user.
    """

    serializer_class = UserSerializer

    @extend_schema(request=UserSerializer)
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = get_user_model().objects.create_user(**serializer.validated_data)
            token, _ = Token.objects.get_or_create(user=user)
            val = {"user": serializer.data, "token": token.key}
            return Response(val, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateTokenView(ObtainAuthToken):
    """
    Retrieve authentication token.
    """

    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
