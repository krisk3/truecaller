from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status

# Create your tests here.


class CreateUserViewTest(APITestCase):
    """Tests for creating a new user."""

    def setUp(self):
        """Setup test environment."""
        self.client = APIClient()
        self.url = reverse("user:create-user")

    def test_create_successful_valid_user(self):
        """Test that ensures creation of a new user with valid payload is successful."""
        payload = {
            "phone": "1234567890",
            "name": "Test User",
            "password": "testpass123",
            "email": "test@example.com",
        }
        res = self.client.post(self.url, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data["user"])
        self.assertTrue(user.check_password(payload["password"]))

    def test_user_exists(self):
        """Test that ensures a new user cannot be created if it already exists."""
        payload = {"phone": "1234567890", "name": "Test", "password": "testpass123"}
        get_user_model().objects.create_user(**payload)
        res = self.client.post(self.url, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that ensures a new user cannot be created with a short password"""
        payload = {"phone": "1234567890", "name": "Test", "password": "pw"}
        res = self.client.post(self.url, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(phone=payload["phone"]).exists()
        self.assertFalse(user_exists)


class CreateTokenViewTest(APITestCase):
    def setUp(self):
        """Setup test environment."""
        self.client = APIClient()
        self.url = reverse("user:find-token")

    def test_create_token_for_user(self):
        """Test that ensures a valid token is created for a validated user."""
        payload = {"phone": "1234567890", "name": "Test", "password": "testpass123"}
        get_user_model().objects.create_user(**payload)
        res = self.client.post(self.url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("token", res.data)

    def test_create_token_invalid_credentials(self):
        """Test that ensures that an auth token is not created for invalid credentials."""
        get_user_model().objects.create_user(
            phone="1234567890", name="Test", password="testpass123"
        )
        payload = {"phone": "1234567890", "password": "wrong"}
        res = self.client.post(self.url, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("token", res.data)

    def test_create_token_missing_field(self):
        """Test that ensures that an auth token is not created for when required fields are missing."""
        res = self.client.post(self.url, {"phone": "1234567890"})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("token", res.data)
