from aiogram import Router, F, types
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.fsm.context import FSMContext

from bot_config import database

hw_router = Router()

class HomeWork(StatesGroup):
    name = State()
    group = State()
    hw_num = State()
    repoz = State()

@hw_router.callback_query(F.data == "hw", default_state)
async def start_review(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(HomeWork.name)
    await callback_query.message.answer("Как вас зовут?")

@hw_router.message(HomeWork.name)
async def process_name(message: types.Message, state: FSMContext):
    msg = message.text
    if len(msg) > 15:
        await message.answer("Имя слишком длинное!")
        return
    await state.update_data(name=message.text)
    await state.set_state(HomeWork.group)
    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(text="Group 47-1"),
                types.KeyboardButton(text="Group 47-2"),
                types.KeyboardButton(text="Group 47-3"),
            ]
        ]
    )
    await message.answer("Выберите группу", reply_markup=kb)

@hw_router.message(HomeWork.group, F.text.in_(["Group 47-1", "Group 47-2", "Group 47-3"]))
async def process_group(message: types.Message, state: FSMContext):
    await state.update_data(group=message.text)
    await state.set_state(HomeWork.hw_num)
    kb = types.ReplyKeyboardRemove()
    await message.answer("Выберите номер ДЗ\n"
                         "От 1 до 8", reply_markup=kb)


@hw_router.message(HomeWork.hw_num)
async def process_hw_num(message: types.Message, state: FSMContext):
    num = message.text
    if not num.isdigit() or int(num) < 1 or int(num) > 8:
        await message.answer("Вводите только цифры от 1 до 8!")
        return
    await state.update_data(hw_num=message.text)
    await state.set_state(HomeWork.repoz)
    await message.answer("Введите ссылку на репозиторий")

@hw_router.message(HomeWork.repoz)
async def process_repoz(message: types.Message, state: FSMContext):
    await state.update_data(repoz=message.text)
    await message.answer("ДЗ добавлено!")
    data = await state.get_data()
    print(data)
    await state.clear()

    database.execute(
        query="INSERT INTO homeworks (name, group_name, hw_num, repoz) VALUES (?, ?, ?, ?) ",
        params=(data["name"], data["group"], data["hw_num"], data["repoz"]),
    )