"""
Define functions and classes to respond to client requests.
"""

from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes


from .serializers import SpamNumberSerializer, ContactSerializer
from .models import SpamContact, Contact


class SpamNumberView(APIView):
    """Mark a number as spam."""

    permission_classes = [IsAuthenticated]
    aunthentication_classes = [TokenAuthentication, BasicAuthentication]
    serializer_class = SpamNumberSerializer

    @extend_schema(request=SpamNumberSerializer)
    def post(self, request):
        serializer = SpamNumberSerializer(data=request.data)
        if serializer.is_valid():
            number = serializer.validated_data["phone"]
            current_user = request.user

            spam_contact, created = SpamContact.objects.get_or_create(spam_phone=number)

            if created:
                spam_contact.spammed_by_users.set([current_user])
                return Response({'message': 'Successfully marked spam.', 'phone': number}, status=status.HTTP_201_CREATED)
            else:
                spam_contact.spammed_by_users.add(current_user)
                return Response({'message': 'Successfully marked spam.', 'phone': number}, status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SearchNameView(APIView):
    """Search for a contact by name."""

    permission_classes = [IsAuthenticated]
    aunthentication_classes = [TokenAuthentication, BasicAuthentication]
    serializer_class = ContactSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="name",
                description="Name to search for",
                required=True,
            )
        ],
        request=ContactSerializer,
    )
    def get(self, request):
        name = request.query_params.get("name", "")
        startswith_name = Contact.objects.filter(contact_name__istartswith=name)
        contains_name = Contact.objects.filter(
            ~Q(contact_name__istartswith=name), contact_name__icontains=name
        )
        results = startswith_name.union(contains_name)

        serializer = ContactSerializer(results, many=True)
        return Response(serializer.data)


class ContactSearchView(APIView):
    """Search for a contact by phone number."""

    permission_classes = [IsAuthenticated]
    aunthentication_classes = [TokenAuthentication, BasicAuthentication]
    serializer_class = ContactSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="phone_number",
                description="Phone number to search for",
                required=True,
            )
        ],
        request=ContactSerializer,
    )
    def get(self, request):
        phone_number = request.query_params.get("phone_number", "")
        print(phone_number)
        user_exists = get_user_model().objects.filter(phone=phone_number).exists()

        if user_exists:
            results = Contact.objects.filter(
                contact_phone=phone_number, user__phone=phone_number
            )
        else:
            results = Contact.objects.filter(contact_phone=phone_number)
        serializer = ContactSerializer(results, many=True, context={"request": request})
        return Response(serializer.data)
