import functools
from contextlib import suppress

import requests
from aiogram import Bot, Dispatcher, F, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from asgiref.sync import sync_to_async
from django.conf import settings

from apps.bot.models import TgUser
from apps.orders.models import Order
from apps.users.models import User

dp = Dispatcher()


@functools.cache
def bot() -> Bot:
    return Bot(token=settings.TELEGRAM_BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


def db(tg_user):
    return tg_user.user.id


def order_to_item(order):
    result = []
    for i in order.order_rows.all():
        result.append(f"{i.item.catalog.name}, на общую сумму: {i.sum_current_order} руб.")
    return result


async def all_purchases(chat_id, tg_user):
    user_id = await sync_to_async(db)(tg_user)
    await bot().send_message(chat_id, "На текущий момент ваши покупки:")
    async for order in Order.objects.filter(user_id=user_id).all():
        await bot().send_message(chat_id, f" Заказа №{order.id}: <b>{await sync_to_async(order_to_item)(order)}</b>")


@dp.message(Command("pay"))
async def any_message(message: Message):
    tg_user = await TgUser.objects.filter(id=message.from_user.id).afirst()
    if not tg_user:
        await message.answer("еще я вас знаю, выполните /start")
    else:
        await all_purchases(message.from_user.id, tg_user)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        f"Привет, {html.bold(message.from_user.full_name)}! Введи свою почту, чтобы я нашел тебя в <b>skillsup</b>"
    )


@dp.message(F.text)
async def get_email(message: Message) -> None:
    email = message.text
    tg_user = await TgUser.objects.filter(user__email=email, id=message.from_user.id).afirst()
    if tg_user:
        answer = "уже все хорошо, я тебя помню, буду присылать уведомления"

    else:
        user = await User.objects.filter(email=email).afirst()
        if user:
            try:
                await TgUser.objects.acreate(
                    user=user,
                    id=message.from_user.id,
                    username=message.from_user.username,
                )
                answer = "все хорошо, буду присылать уведомления"
            except:  # noqa: E722
                answer = "что-то пошло не так, попробуйте позднее"
        else:
            answer = "либо ошибся в email, либо еще не зарегистрирован в нашей системе"
    await message.answer(answer)


def pay_items(user_email, order_id: str):
    tg_user_id = TgUser.objects.get(user__email=user_email).id
    with suppress(Exception):
        resp = requests.post(
            f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage",
            json={"chat_id": tg_user_id, "text": f"Вы только что оплатили заказ №: {order_id}"},
        )
    print(resp.text)


async def main() -> None:
    await dp.start_polling(bot())
