import hmac

import requests

from .models import Order


class LeadpayError(Exception):
    pass


def calc_payload_hash(payload: dict, secret: str) -> str:
    raw_value = "".join([x[1] for x in sorted(payload.items())])
    return hmac.new(secret.encode("utf-8"), raw_value.encode("utf-8"), "sha256").hexdigest()


def generate_leadpay_payment_link(order: Order) -> str:
    payload = dict(
        login="demo-login",
        id=str(order.id),
        product_name=order.user.catalogs.first().name,
        product_price=str(order.sum_total_all_orders),
        count="1",
        email=order.user.email,
        phone="+79991112233",
        fio=order.user.get_full_name(),
        notification_url="http://localhost/api/v1/leadpay-notification/",
    )

    payload["hash"] = calc_payload_hash(payload, "SECRET66666")

    # Делаем фейковый Post-запрос на адрес (якобы платежного Шлюза)
    response = requests.post(
        "http://localhost:8000/api/v1/fake-leadpay-link/",  # https://app.leadpay.ru/api/v2/getLink/
        json=payload,
    )
    if response.status_code != 200:
        try:
            error = response.json()["description"]
        except Exception as ex:
            raise LeadpayError(f"Unexpected error in Leadpay: {ex}")
        raise LeadpayError(error)

    fake_link = response.json()["url"]
    print("Запрос отправлен. Ссылка получена:")
    print(fake_link)
    return fake_link
