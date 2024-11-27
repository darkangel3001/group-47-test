from aiogram import Router, types
from aiogram.filters import Command

start_router = Router()

@start_router.message(Command('start'))
async def start(message: types.Message):
    msg = F"Привет {message.from_user.username}!"
    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(
                text="Отправить ДЗ",
                callback_data="hw"
            )
            ]
        ]
    )
    await message.answer(msg, reply_markup=kb)