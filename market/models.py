from django.db import models

from accounts.models import User


class BaseModel:
    timestamp = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    last_modifier = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False)


class ProductType(models.Model, BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Vendor(models.Model, BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model, BaseModel):
    # timestamp = models.DateTimeField(auto_now_add=True)
    # last_modified = models.DateTimeField(auto_now=True)
    # last_modifier = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False)
    type = models.ForeignKey(ProductType, on_delete=models.SET_NULL, null=True, blank=False)
    name = models.CharField(max_length=255)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=False)
    price = models.BigIntegerField()

    def __str__(self):
        return self.name


class Shop(models.Model, BaseModel):
    # timestamp = models.DateTimeField(auto_now_add=True)
    # last_modified = models.DateTimeField(auto_now=True)
    # last_modifier = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=511)
    latitude = models.DecimalField(max_digits=10, decimal_places=6)
    longitude = models.DecimalField(max_digits=10, decimal_places=6)

    def __str__(self):
        return self.name


class Inventory(models.Model, BaseModel):

    class Meta:
        verbose_name_plural = "Inventories"

    shop = models.ForeignKey(Shop, on_delete=models.SET_NULL, null=True, blank=False)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=False)
    quantity = models.PositiveIntegerField()
    price = models.BigIntegerField()

    def __str__(self):
        return self.shop.__str__() + ": " + self.product.__str__() + " (" + str(self.quantity) + ")"
