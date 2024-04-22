from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.api.serializers.orders import OrderSerializer
from apps.api.views.abstract_dynamic import BaseModelViewSet
from apps.orders.models import Order
from apps.orders.service_pay import LeadpayError, generate_leadpay_payment_link


class OrderViewSet(BaseModelViewSet):
    http_method_names = [
        "get",
        "post",
        "head",
        "options",
        "patch",
    ]  # Get на сущность, Get на список, Patch на сущность. Post - разрешили, но сам create - нужно запретить

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, queryset=None):
        qs = super().get_queryset()
        result = qs.filter(user_id=self.request.user.id)
        return result

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(methods=["post"], detail=False, permission_classes=[IsAuthenticated])
    def checkout(self, request):
        user = request.user
        basket = request.user.baskets.first()

        if not basket:
            raise ValidationError("user hasn't basket", code="no-basket")

        if not basket.basket_rows.exists():
            raise ValidationError("user hasn't products in the basket", code="no-products-in-basket")

        for row in basket.basket_rows.all():
            if row.qty > row.item.count:
                raise ValidationError(f"item is out of stock - {row.item.catalog.name}", code="no-products-in-basket")

            if not row.item.is_active:
                raise ValidationError(
                    f"На текущий момент - Товар:{row.item.catalog.name} отсутствует а складе",
                    code="no-products",
                )

        # транзакция - для безопасного кода
        with transaction.atomic():
            order = Order.objects.create(user=user)
            for row in basket.basket_rows.all():
                order.order_rows.create(item=row.item, qty=row.qty, price=row.item.price)
            basket.basket_rows.all().delete()  # Очищаем корзину

        serializer = self.get_serializer(order)
        # serializer = OrderSerializer(order)  # Выводим через сериализатор итог покупок
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=["get"], detail=True, url_path="payment-link")
    def payment_link(self, request, *args, **kwargs):
        obj = self.get_object()

        try:
            print("отправил объект в функцию")
            link = generate_leadpay_payment_link(obj)
        except LeadpayError as ex:
            raise APIException(detail=str(ex), code=status.HTTP_424_FAILED_DEPENDENCY)

        return Response({"link for pay: ": link}, status=status.HTTP_200_OK)


# Создали Фейковый адрес (якобы Шлюза для отправки Post-запроса на получения ссылки для оплаты)
@api_view(http_method_names=["post"])
@permission_classes([AllowAny])
def fake_leadpay_link(request, *args, **kwargs):
    data = request.data
    link_result_pay = {"url": f'http://{data["login"]}.ru/id-{data["id"]}/{data["hash"]}'}
    return Response(link_result_pay, status=status.HTTP_200_OK)
