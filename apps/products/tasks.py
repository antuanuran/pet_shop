from celery.app import shared_task
from django.core.files.base import File

from apps.products import service_pdf


@shared_task(autoretry_for=(Exception,), max_retries=1)
def celery_generate_result(order_id: int, user_id: int):
    from apps.orders.models import Order
    from apps.products.models import Cheque
    from apps.users.models import User

    user = User.objects.get(id=user_id)
    order = Order.objects.get(id=order_id)

    pdf_data = service_pdf.generate_pdf(order, user)
    print(pdf_data)
    Cheque.objects.create(order=order, user=user, pdf=File(pdf_data, name=f"{user.email}.pdf"))
