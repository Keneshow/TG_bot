import asyncio
import os
import keyboards as kb
import service as service
from state import App, Drive

from keyboards import main_page_keyboard
from aiogram.fsm.state import StatesGroup, State
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from dotenv import load_dotenv
from callback import *




load_dotenv()

TOKEN = os.getenv("BOT_SCHOOL")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)


class AdminReply(StatesGroup):
    waiting_for_text = State()

@dp.message(StateFilter(AdminReply.waiting_for_text))
async def admin_reply_entry(message: types.Message, state: FSMContext):
    await process_admin_reply(message, state)



@dp.message(CommandStart())
async def start_command(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username
    await message.answer(f"👤 Ваш Telegram ID: {user_id}\n🔗 Ник: @{username}")
    await message.answer(" Добро пожаловать в автошколу!", reply_markup=kb.main_page_keyboard)
    await message.answer("Написать админу", reply_markup=kb.get_contact_and_location_keyboard())


@dp.message(Command(commands='app'))
async def about_app(message: Message, state: FSMContext):
    await state.set_state(App.name)
    await message.answer("Напишите ваше Ф.И.О")

@dp.message(Command(commands='drive'))
async def process_drive(message: Message, state: FSMContext):
    await state.set_state(Drive.d_name)
    await message.answer("напишите ваше Ф.И.О")


@dp.message(F.text)
async def message_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await service.handle_app(message, state)

        await service.handle_drive(message, state)

    if message.text == "Заявки":
        await state.set_state(App.name)
        await message.answer("Напишите ваше Ф.И.О")

    elif message.text == "Вождение":
        await state.set_state(Drive.d_name)
        await message.answer("напишите ваше Ф.И.О")



async def main():
    dp.callback_query.register(show_price, F.data == "show_price")
    dp.callback_query.register(reply_to_user, F.data.regexp(r"^reply_(\d+)$"))
    dp.callback_query.register(admin_callback_handler, F.data.regexp(r"^(processed|delete)_(\d+)$"))
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
