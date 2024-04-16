from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from apps.api.serializers.items import ItemSerializer
from apps.api.views.abstract_dynamic import BaseModelViewSet
from apps.products.models import Item


class ItemViewSet(BaseModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self, queryset=None):
        qs = super().get_queryset(queryset)
        return qs

    @action(detail=True, methods=["post"], url_path="change-favourite", permission_classes=[IsAuthenticated])
    def change_favourite(self, request, *args, **kwargs):
        item = self.get_object()
        user = self.request.user

        if item.favourites.filter(id=user.id).exists():
            item.favourites.remove(user)

        else:
            item.favourites.add(user)

        my_serializer = self.get_serializer(instance=item)
        return Response(my_serializer.data)
