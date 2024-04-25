from contextlib import suppress

import requests
from aiogram import Bot, Dispatcher, F, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message
from django.conf import settings

from apps.bot.models import TgUser
from apps.orders.models import Order
from apps.users.models import User

dp = Dispatcher()
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


async def all_purchases(user_id, email):
    async for order in Order.objects.filter(user__email=email).all():
        await bot.send_message(user_id, f" Заказ № {order.id}")


@dp.message(Command("pay"))
async def any_message(message: Message):
    await message.answer(f"Так, {html.bold(message.from_user.full_name)}, введи свою почту:")


@dp.message(F.text)
async def purchases_func(message: Message) -> None:
    email = message.text
    tg_user = await TgUser.objects.filter(user__email=email, id=message.from_user.id).afirst()
    if tg_user:
        answer = "почту я твою уже знаю, щас пришлю твои покупки"

    else:
        user = await User.objects.filter(email=email).afirst()
        if user:
            try:
                await TgUser.objects.acreate(
                    user=user,
                    id=message.from_user.id,
                    username=message.from_user.username,
                )
                answer = "почту принял. Высылаю твои покупки:"
            except:  # noqa: E722
                answer = "что-то пошло не так, попробуйте позднее"
        else:
            answer = "либо ошибся в email, либо еще не зарегистрирован в нашей системе"
    await message.answer(answer)

    user_id = message.from_user.id
    await all_purchases(user_id, email)


def pay_items(user_email, item, price):
    tg_user_id = TgUser.objects.get(user__email=user_email).id
    with suppress(Exception):
        requests.post(
            f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage",
            json={"chat_id": tg_user_id, "text": f' Вы приобрели: "{item}" по цене:{price}'},
        )


async def main() -> None:
    await dp.start_polling(bot)
