from datetime import date

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from core.models import BaseModel


class Category(BaseModel):
    """A model for the category of the product."""

    name = models.CharField(
        max_length=50,
        unique=True,
        help_text="Name of the category (e.g., SUV, Sedan, Truck)",
    )
    description = models.TextField(blank=True, default="")

    class Meta:
        db_table = "categories"
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return self.name


class Manufacturer(BaseModel):
    """A model for the manufacturer of the product."""

    name = models.CharField(
        max_length=50, unique=True, help_text="Name of the manufacturer (e.g., Toyota)"
    )
    description = models.TextField(blank=True, default="")

    class Meta:
        db_table = "manufacturers"
        verbose_name = "Manufacturer"
        verbose_name_plural = "Manufacturers"

    def __str__(self) -> str:
        return self.name


class Model(BaseModel):
    """A model for the make and model of the product."""

    manufacturer = models.ForeignKey(
        to=Manufacturer, on_delete=models.CASCADE, related_name="models"
    )
    name = models.CharField(
        max_length=50, help_text="Model name (e.g., Corolla, Mustang)"
    )
    description = models.TextField(blank=True, default="")

    class Meta:
        db_table = "manufacturer_models"
        verbose_name = "Manufacturer Model"
        verbose_name_plural = "Manufacturer Models"

    def __str__(self) -> str:
        return f"{self.manufacturer} {self.name}"


class Car(BaseModel):
    """A model for cars with detailed specifications."""

    class ConditionChoices(models.TextChoices):
        """Choices for the condition field."""

        NEW = "new", "New"
        USED = "used", "Used"

    class TransmissionChoices(models.TextChoices):
        """Choices for the transmission field."""

        AUTOMATIC = "automatic", "Automatic"
        MANUAL = "manual", "Manual"

    class FuelTypeChoices(models.TextChoices):
        """Choices for the fuel_type field."""

        PETROL = "petrol", "Petrol"
        DIESEL = "diesel", "Diesel"
        ELECTRIC = "electric", "Electric"
        GAS = "gas", "Gas"

    car_model = models.ForeignKey(
        to=Model,
        on_delete=models.CASCADE,
        help_text="Model name (e.g., Corolla, Mustang)",
        related_name="cars",
        related_query_name="car",
    )
    year = models.PositiveIntegerField(
        help_text="Year of manufacture",
        default=2021,
        validators=[MinValueValidator(1900), MaxValueValidator(date.today().year)],
    )
    mileage = models.PositiveIntegerField(
        help_text="Number of kilometers driven",
        default=0,
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Selling price in Egyptian pounds",
    )
    condition = models.CharField(
        max_length=20,
        choices=ConditionChoices.choices,
        default=ConditionChoices.NEW,
        help_text="New or used",
    )
    fuel_type = models.CharField(
        max_length=50,
        choices=FuelTypeChoices.choices,
        default=FuelTypeChoices.PETROL,
        help_text="Fuel type (e.g., Petrol, Diesel, Electric)",
    )
    transmission = models.CharField(
        max_length=20,
        choices=TransmissionChoices.choices,
        help_text="Transmission type (e.g., Manual, Automatic).",
        default=TransmissionChoices.AUTOMATIC,
    )
    color = models.CharField(max_length=50, help_text="Color of the vehicle")
    engine_capacity = models.DecimalField(
        decimal_places=2,
        max_digits=4,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
        default=0.0,
        help_text="Engine capacity in liters",
    )
    category = models.ManyToManyField(to=Category, related_name="cars")

    class Meta:
        db_table = "products"
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["-year"]
        indexes = [
            models.Index(fields=["price"]),
            models.Index(fields=["year"]),
        ]

    def __str__(self) -> str:
        return f"{self.car_model} ({self.year}) - {self.condition} - {self.color} - ${self.price}"

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        super().save(*args, **kwargs)
