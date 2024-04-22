# Generated by Django 4.1.13 on 2024-04-22 01:57

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("holder", "0001_initial"),
        ("products", "0006_item_favourites"),
    ]

    operations = [
        migrations.CreateModel(
            name="Review",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("text", models.TextField()),
                ("rating", models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(10)])),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="reviews", to=settings.AUTH_USER_MODEL
                    ),
                ),
                ("images", models.ManyToManyField(blank=True, related_name="+", to="holder.imageholder")),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="reviews", to="products.item"
                    ),
                ),
                ("videos", models.ManyToManyField(blank=True, related_name="+", to="holder.videoholder")),
            ],
            options={
                "verbose_name": "отзыв",
                "verbose_name_plural": "отзывы к товару",
            },
        ),
    ]
