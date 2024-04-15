from django.core.validators import MinValueValidator
from django.db import models

from apps.users.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    # products

    class Meta:
        verbose_name = "1. Категория"
        verbose_name_plural = "1. Категории"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    # catalogs

    class Meta:
        verbose_name = "2. Продукт"
        verbose_name_plural = "2. Продукты"

    def __str__(self):
        return f"{self.name}"


class Catalog(models.Model):
    name = models.CharField(max_length=100, unique=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="catalogs")
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name="catalogs")

    class Meta:
        verbose_name = "3. Каталог"
        verbose_name_plural = "3. Каталоги"

    def __str__(self):
        return self.name


class Attribute(models.Model):
    name = models.CharField(max_length=100)
    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE, related_name="attributes")
    # itemattributes

    class Meta:
        verbose_name = "Атрибут"
        verbose_name_plural = "Атрибуты"

    def __str__(self):
        return f"{self.name}: [{self.catalog.name}]"


class Item(models.Model):
    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE, related_name="items")
    price = models.IntegerField(validators=[MinValueValidator(1)])
    count = models.PositiveIntegerField()
    upc = models.CharField(max_length=64, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    # itemattributes

    @property
    def attributes(self):
        result = []
        for i in self.itemattributes.all():
            result.append(f"{i.attribute.name}: {i.value}")
        return result

    class Meta:
        verbose_name = "4. Товар"
        verbose_name_plural = "4. Товары"
        constraints = [
            models.UniqueConstraint(fields=["catalog", "upc"], name="unique_item_name_per_upc"),
        ]

    def __str__(self):
        return f"{self.catalog}. Цена: {self.price} руб. / Кол-во: {self.count} шт."


class ItemAttribute(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name="itemattributes")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="itemattributes")
    value = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Конкретный параметр"
        verbose_name_plural = "Конкретные параметры"

    def __str__(self):
        return self.value
