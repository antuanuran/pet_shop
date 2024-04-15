from rest_framework import status
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.products.service import import_data


@api_view(http_method_names=["post"])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser])
def import_file(request):
    if not request.FILES or "file" not in request.FILES:
        raise ValidationError("no file", code="no-file")

    data_stream = request.FILES["file"]
    data_stream = data_stream.read().decode()
    import_data(data_stream, request.user.id)

    return Response(
        data=f"file: '{request.FILES['file'].name}' LOAD......ok",
        status=status.HTTP_201_CREATED,
    )
