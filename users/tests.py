from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from users.models import Profile


class ProfileModelTest(TestCase):
    """Test the Profile model."""

    def setUp(self):
        """Set up the test."""
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@mail.com",
            password="testpassword",
            first_name="test",
            last_name="user",
        )

    def test_profile_str(self):
        """Test the __str__ method of the Profile model."""
        profile = Profile.objects.create(
            user=self.user, role=Profile.RoleChices.ADMIN, phone_number="1234567890"
        )
        self.assertEqual(str(profile), self.user.username)

    def test_new_profile_without_passing_a_role(self):
        """Test creating a new profile without passing a role"""
        profile = Profile.objects.create(user=self.user)
        self.assertEqual(profile.role, Profile.RoleChices.CUSTOMER)

    def test_new_profile_with_a_role_not_in_the_role_choices(self):
        """Test creating a new profile with passing a role"""
        profile = Profile(user=self.user, role="test")
        with self.assertRaises(ValidationError):
            profile.save()

    def test_profile_with_phone_number_more_than_15_characters(self):
        """Test creating a new profile with phone number more than 15 characters"""
        profile = Profile(user=self.user, phone_number="1234567890123456")
        with self.assertRaises(ValidationError):
            profile.save()

    def test_two_profiles_with_same_user(self):
        """Test creating two profiles with the same user"""
        Profile.objects.create(user=self.user)
        with self.assertRaises(ValidationError):
            Profile.objects.create(user=self.user)

    def test_cascade_delete_user(self):
        """Test deleting a user should delete the profile"""
        Profile.objects.create(user=self.user)
        self.user.delete()
        self.assertEqual(Profile.objects.count(), 0)
