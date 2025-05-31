from telethon import TelegramClient, events
import asyncio

# Вставь свои API_ID и API_HASH в переменные окружения Railway (API_ID и API_HASH)

import os

api_id = 21800053
api_hash = '59f47ce469b1874fbba2adcaf2ee7212' 

client = TelegramClient('ritual_bot_session', api_id, api_hash)

# Скрипты общения и логика

WELCOME_MESSAGE = (
    "Привет! Я помогу с ритуалами. Чем могу помочь?\n"
    "Если хочешь узнать разницу ритуалов, напиши 'разница'.\n"
    "Чтобы оплатить — просто скажи 'хочу оплатить'."
)

RITUAL_DIFF = (
    "Есть разные ритуалы:\n"
    "1) Привлечение любви — работает на чувства.\n"
    "2) Защита — оберегает от негатива.\n"
    "3) Удача — улучшает судьбу.\n"
    "Если хочешь подробнее, спрашивай."
)

PAYMENT_REPLY = (
    "Отличный выбор! Попозже скину реквизиты куда нужно будет перевести.\n"
    "В какой валюте вам будет удобно заплатить?\n"
    "А еще, прежде чем вы заплатите, хочу рассказать о нескольких вещах, которые нельзя делать после ритуала:\n"
    "1) гадать на этого человека или сверху делать еще ритуалы\n"
    "2) пить и употреблять\n"
    "3) рассказывать кому-либо об этом, даже лучшей подруге\n"
    "4) думать, что ничего не сработает, создавая энергетические блоки\n"
    "5) не проявляться первой — но это не значит, что нужно слать парня, просто не бегать за ним как собачка первой."
)

# ID второго аккаунта, куда пересылать данные
FORWARD_TO_ID = 6353198979

# Словарь для хранения состояния клиента (чтобы не отвечать после оплаты)
paid_clients = set()

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    sender = await event.get_sender()
    sender_id = sender.id
    text = event.text.lower()

    # Если клиент уже оплатил, игнорируем дальнейшие сообщения
    if sender_id in paid_clients:
        return

    # Приветствие при первом сообщении
    if text in ('привет', 'здравствуйте', 'hello', 'hi'):
        await event.reply(WELCOME_MESSAGE)
        return

    # Разница ритуалов
    if 'разница' in text:
        await event.reply(RITUAL_DIFF)
        return

    # Клиент хочет оплатить
    if 'хочу оплатить' in text or 'оплатить' in text:
        await event.reply(PAYMENT_REPLY)

        # Пересылаем инфо о клиенте и сообщении на второй аккаунт
        msg_info = f"Клиентка: {sender.first_name} (ID: {sender_id})\nСообщение: {event.text}\nСсылка: https://t.me/c/{event.chat_id}/{event.id}"
        try:
            await client.send_message(FORWARD_TO_ID, msg_info)
        except Exception as e:
            print(f"Ошибка при пересылке: {e}")

        paid_clients.add(sender_id)
        return

    # Если пишут "расклад" или про гадание — пересылаем к коллеге Марсу
    if 'расклад' in text or 'гадание' in text:
        await event.reply("Я не делаю расклады, пожалуйста, обратись к коллеге Марсу — @https_m4rs")
        return

    # Если ничего не понял — стандартный ответ
    await event.reply("Извини, я тебя не совсем понял. Можешь сформулировать иначе?")

async def main():
    await client.start()
    print("Бот запущен...")
    await client.run_until_disconnected()

if __name__ == "__main__": 
    import asyncio
    asyncio.run(main())
