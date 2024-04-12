from django.core.validators import MinValueValidator
from django.db import models


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
    # attributes
    # items

    class Meta:
        verbose_name = "2. Продукт"
        verbose_name_plural = "2. Продукты"

    def __str__(self):
        return f"{self.name}"


class Attribute(models.Model):
    name = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="attributes")
    # itemattributes

    class Meta:
        verbose_name = "Атрибут"
        verbose_name_plural = "Атрибуты"

    def __str__(self):
        return f"{self.name}: [{self.product.name}]"


class Item(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="items")
    price = models.IntegerField(validators=[MinValueValidator(1)])
    count = models.PositiveIntegerField()
    upc = models.CharField(max_length=64, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    # itemattributes

    class Meta:
        verbose_name = "3. Товар"
        verbose_name_plural = "3. Товары"

    def __str__(self):
        return f"{self.product}. Цена: {self.price} руб. / Кол-во: {self.count} шт."


class ItemAttribute(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name="itemattributes")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="itemattributes")
    value = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Конкретный параметр"
        verbose_name_plural = "Конкретные параметры"

    def __str__(self):
        return self.value
