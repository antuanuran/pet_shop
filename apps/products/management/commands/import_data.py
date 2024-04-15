import csv

from django.core.management import BaseCommand

from apps.products.service import load_result


def import_console(data, admin_id):
    data_stream = csv.DictReader(data, delimiter=",")
    load_result(data_stream, admin_id)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("path")
        parser.add_argument("--admin_id")

    def handle(self, path, *args, **options):
        with open(path, "r") as file:
            import_console(file, options["admin_id"])


# python manage.py import_data data_all/import.csv --admin_id 1
