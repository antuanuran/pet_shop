from django.core.exceptions import ValidationError
from django.db import models

from apps.products.models import Item
from apps.users.models import User


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="baskets")
    items = models.ManyToManyField(
        Item, through="BasketRow", related_name="baskets", blank=True
    )  # Не обязательно, но в будущем может сократить запросы к товарам через корзину
    # basket_rows

    @property
    def total_price_all_basket(self):
        total = 0
        for row in self.basket_rows.all():
            total += row.summa_price
        return total

    @property
    def number_baskets(self):
        text = f"Корзина ({self.user})"
        return text

    class Meta:
        verbose_name = "Корзина товаров"
        verbose_name_plural = "Корзина товаров"

    def __str__(self):
        return self.user.email


class BasketRow(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name="basket_rows")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="basket_rows")
    qty = models.PositiveIntegerField(default=1)

    @property
    def summa_price(self):
        return self.qty * self.item.price

    @property
    def price_unit(self):
        return self.item.price

    @property
    def is_active_item(self):
        if self.item.is_active:
            return True
        else:
            return False

    # ******************************
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def clean(self):
        if not self.item.is_active:
            raise ValidationError({"item not active!"}, code="not-active-item")

    # ******************************

    class Meta:
        verbose_name = "заказ в корзине"
        verbose_name_plural = "заказы в корзине"

    def __str__(self):
        return f" {self.item}"
