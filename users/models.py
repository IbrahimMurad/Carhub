""" This module contains the models for the users app.
"""

from django.contrib.auth.models import User
from django.db import models

from core.models import BaseModel

# class Address(models.Model):
#     """a model for the address of the user."""

#     Country = models.CharField(max_length=50)
#     city = models.CharField(max_length=50)
#     address = models.CharField(max_length=50)
#     postal_code = models.CharField(max_length=10)

#     class Meta:
#         db_table = "addresses"
#         verbose_name = "Address"
#         verbose_name_plural = "Addresses"

#     def __str__(self):
#         return self.address + ", " + self.city + ", " + self.Country


class Profile(BaseModel):

    class RoleChices(models.TextChoices):
        """choices for the role field."""

        ADMIN = "admin", "Admin"
        CUSTOMER = "Customer", "Customer"
        SELLER = "seller", "Seller"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(
        max_length=20, choices=RoleChices.choices, default=RoleChices.CUSTOMER
    )
    # address = models.OneToOneField("Address", blank=True, null=True)

    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
