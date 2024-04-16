from apps.api.serializers.baskets import BasketRowSerializer
from apps.api.views.abstract_dynamic import BaseModelViewSet
from apps.baskets.models import Basket, BasketRow


class BasketRowViewSet(BaseModelViewSet):
    queryset = BasketRow.objects.all()
    serializer_class = BasketRowSerializer

    def perform_create(self, serializer):
        basket, _ = Basket.objects.get_or_create(user_id=self.request.user.id)
        serializer.save(basket_id=basket.id)

    def get_queryset(self, queryset=None):
        qs = super().get_queryset()
        result = qs.filter(basket__user_id=self.request.user.id)
        return result
