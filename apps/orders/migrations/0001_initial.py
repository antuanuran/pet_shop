# Generated by Django 4.1.13 on 2024-04-15 08:01

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("products", "0004_item_description"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("новый", "Status New"),
                            ("в доставке", "Status Delivery"),
                            ("завершен", "Status Finished"),
                            ("отменен", "Status Canceled"),
                        ],
                        default="новый",
                        max_length=30,
                    ),
                ),
                ("created_at", models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="orders", to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
            options={
                "verbose_name": "Покупка / Заказ",
                "verbose_name_plural": "Покупки / Заказы",
            },
        ),
        migrations.CreateModel(
            name="OrderRow",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("qty", models.PositiveIntegerField()),
                ("price", models.PositiveIntegerField()),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="order_rows", to="products.item"
                    ),
                ),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="order_rows", to="orders.order"
                    ),
                ),
            ],
            options={
                "verbose_name": "Покупка / Заказ",
                "verbose_name_plural": "Покупки / Заказы",
            },
        ),
    ]
