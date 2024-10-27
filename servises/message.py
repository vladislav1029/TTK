import asyncio
from aiogram.types import Message


async def answer_delete(message: Message, text: str, time: int = 5):
    send = await message.answer(text=text, parse_mode="HTML")
    await asyncio.sleep(time)
    await send.delete()


async def message_user_delete(message: Message, time: int = 5):

    await asyncio.sleep(time)
    await message.delete()
