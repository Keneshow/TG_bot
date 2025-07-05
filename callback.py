
from aiogram.fsm.state import StatesGroup, State
from aiogram import Bot, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ParseMode

class AdminReply(StatesGroup):
    waiting_for_text = State()


async def show_price(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(
        "📋 *Прайс и время обучения:*\n\n"
        "- 🛵 Категория A — 8,000 сом\n"
        "- 🚗 Категория B — 14,000 сом\n"
        "- 🚛 Категория C — 18,000 сом\n"
        "- 🚘 Вождение — 5,000 сом\n\n"
        "- 🕘 Занятия проходят каждый день с 9:00 до 18:00.",
        parse_mode=ParseMode.MARKDOWN
    )


async def reply_to_user(callback: types.CallbackQuery, state: FSMContext):
    user_id = int(callback.data.split('_')[1])
    await state.update_data(reply_user_id=user_id)
    await state.set_state(AdminReply.waiting_for_text)
    await callback.message.answer("Напишите сообщение для пользователя.")
    await callback.answer()



async def process_admin_reply(message: Message, state: FSMContext):
    data = await state.get_data()
    user_id = data.get('reply_user_id')

    if not user_id:
        await message.answer("Не могу получить ID пользователя для ответа.")
        await state.clear()
        return

    try:
        await message.bot.send_message(user_id, f"Ответ от администратора:\n\n{message.text}")
        await message.answer("Сообщение отправлено пользователю.")
    except Exception as e:
        await message.answer("Не удалось отправить сообщение пользователю.")

    await state.clear()

processed_applications = {}

async def admin_callback_handler(callback: types.CallbackQuery, bot: Bot):
    action, user_id = callback.data.split("_")

    if action == "processed":
        text = callback.message.text  # Сохраняем текст заявки
        processed_applications[user_id] = text
        await bot.send_message(user_id, "Ваша заявка была обработана ✅")
        await callback.answer("✅ Заявка отмечена как обработанная")


    elif action == "delete":
        await callback.message.delete()
        await callback.answer("🗑 Заявка удалена")

    else:
        await callback.answer("⚠️ Неизвестное действие", show_alert=True)