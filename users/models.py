""" This module contains the models for the users app.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models

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


class AdminsManager(models.Manager):
    """a manager for the admins model."""

    def get_queryset(self):
        """returns the queryset for the admins only."""
        return super().get_queryset().filter(role=User.RoleChices.ADMIN)


class CustomersManager(models.Manager):
    """a manager for the customers model."""

    def get_queryset(self):
        """returns the queryset for the customers only."""
        return super().get_queryset().filter(role=User.RoleChices.Customer)


class SellersManager(models.Manager):
    """a manager for the sellers model."""

    def get_queryset(self):
        """returns the queryset for the sellers only."""
        return super().get_queryset().filter(role=User.RoleChices.SELLER)


class User(AbstractUser):

    class RoleChices(models.TextChoices):
        """choices for the role field."""

        ADMIN = "admin", "Admin"
        Customer = "Customer", "Customer"
        SELLER = "seller", "Seller"

    phone_number = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(
        max_length=20, choices=RoleChices.choices, default=RoleChices.Customer
    )
    # address = models.OneToOneField("Address", blank=True, null=True)

    objects = models.Manager()
    admins = AdminsManager()
    customers = CustomersManager()
    sellers = SellersManager()

    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username
