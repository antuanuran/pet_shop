import csv
import os

from rest_framework import status
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.products.service import load_result


def convert_to_csv(data_stream):
    my_file = open("data_all/temp.txt", "w+")
    my_file.write(data_stream)
    my_file.close()

    with open("data_all/temp.txt", "r") as in_file:
        items = []
        for line in in_file:
            str_file = line.strip()
            items.append(str_file.split(","))

        with open("data_all/temp.csv", "w") as out_file:
            writer = csv.writer(out_file)
            writer.writerows(items)

    with open("data_all/temp.csv", "r", encoding="utf-8") as fd:
        data_stream_csv = list(csv.DictReader(fd))

    os.remove("data_all/temp.csv")
    os.remove("data_all/temp.txt")
    return data_stream_csv


@api_view(http_method_names=["post"])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser])
def import_file(request):
    if not request.FILES or "file" not in request.FILES:
        raise ValidationError("no file", code="no-file")

    data_stream = request.FILES["file"]
    data_stream = data_stream.read().decode()
    data_csv = convert_to_csv(data_stream)
    load_result(data_csv, request.user.id)

    return Response(
        data=f"file: '{request.FILES['file'].name}' LOAD......ok",
        status=status.HTTP_201_CREATED,
    )
