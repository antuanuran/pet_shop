import csv

from django.core.management import BaseCommand

from apps.products.models import Catalog, Category, Product


def import_data(data_stream):
    data = csv.DictReader(data_stream, delimiter=",")

    for entity in data:
        category, _ = Category.objects.get_or_create(name=entity["category"])
        product, _ = Product.objects.get_or_create(category_id=category.id, name=entity["product"])
        catalog, _ = Catalog.objects.get_or_create(product_id=product.id, name=entity["catalog"])


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("path")

    def handle(self, path, *args, **options):
        with open(path, "r") as file:
            import_data(file)


# python manage.py import_data data_all/import.csv
