from django.contrib import admin

from product.models import Car, Category, Manufacturer, Model


# Inline model for Model to be displayed within Manufacturer admin
class ModelInline(admin.TabularInline):
    model = Model
    extra = 1


# Custom admin for Manufacturer to include ModelInline
class ManufacturerAdmin(admin.ModelAdmin):
    inlines = [ModelInline]


# Registering models to the admin site
admin.site.register(Category)
admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(Model)
admin.site.register(Car)
