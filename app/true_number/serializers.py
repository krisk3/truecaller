"""
Define serializers for serializing and deserializing data.
"""

from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from django.contrib.auth import get_user_model


from user.validators import phone_validator
from .models import Contact, SpamContact


class SpamNumberSerializer(serializers.Serializer):
    """
    Define a serializer for number.
    """

    phone = serializers.CharField(validators=[phone_validator])


class ContactSerializer(serializers.ModelSerializer):
    """
    Define a serializer for contact model.
    """

    spam_count = serializers.SerializerMethodField()
    spam_likelihood = serializers.SerializerMethodField()
    user_email = serializers.SerializerMethodField()

    class Meta:
        model = Contact
        fields = [
            "contact_name",
            "contact_phone",
            "spam_count",
            "spam_likelihood",
            "user_email",
        ]

    @extend_schema_field(serializers.IntegerField())
    def get_spam_count(self, obj):
        try:
            spam_contact = SpamContact.objects.get(spam_phone=obj.contact_phone)
            return spam_contact.spam_count
        except SpamContact.DoesNotExist:
            return 0

    @extend_schema_field(serializers.CharField())
    def get_spam_likelihood(self, obj):
        spam_count = self.get_spam_count(obj)
        if spam_count == 0:
            return "Not Spam"
        elif spam_count <= 3:
            return "Low"
        elif spam_count <= 10:
            return "Medium"
        else:
            return "High"

    @extend_schema_field(serializers.CharField())
    def get_user_email(self, obj):
        request = self.context.get("request")
        if request and request.user:
            try:
                user = get_user_model().objects.get(phone=obj.contact_phone)
                contacts = Contact.objects.filter(user=user)
                for contact in contacts:
                    if request.user.phone == contact.contact_phone:
                        return obj.user.email
            except:
                get_user_model().DoesNotExist
                return None
        return None
