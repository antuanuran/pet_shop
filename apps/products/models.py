from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager

from apps.holder.models import ImageHolder, VideoHolder
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
    poster = models.ForeignKey(ImageHolder, on_delete=models.CASCADE, related_name="+", null=True, blank=True)
    video = models.ForeignKey(VideoHolder, on_delete=models.CASCADE, related_name="+", null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    upc = models.CharField(max_length=64, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    favourites = models.ManyToManyField(User, related_name="favourites", blank=True)

    tags = TaggableManager(blank=True)
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


class Review(models.Model):
    class Meta:
        verbose_name = "отзыв"
        verbose_name_plural = "отзывы к товару"

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="reviews")
    text = models.TextField()
    images = models.ManyToManyField(ImageHolder, related_name="+", blank=True)
    videos = models.ManyToManyField(VideoHolder, related_name="+", blank=True)
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(10)])
    created_at = models.DateTimeField(default=timezone.now)


class Cheque(models.Model):
    from apps.orders.models import Order

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cheques")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="cheques")
    pdf = models.FileField(upload_to="files/certificates/", max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
