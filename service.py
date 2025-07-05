
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from state import App, Drive
from main import ADMIN_ID


import keyboards as kb



# заявка на обучение


async def delete_prev_qna(message: Message):
    try:
        await message.bot.delete_message(message.chat.id, message.message_id - 1)  # вопрос
        await message.bot.delete_message(message.chat.id, message.message_id)      # ответ
    except:
        pass


async def app_name(message: Message, state: FSMContext):
    await delete_prev_qna(message)
    full_name = message.text.strip()
    await state.update_data(name=full_name)
    await state.set_state(App.phone)
    await message.answer("📞 Напишите ваш номер телефона")

async def app_phone(message: Message, state: FSMContext):
    await delete_prev_qna(message)
    await state.update_data(phone=message.text)
    await state.set_state(App.category)
    await message.answer("Выберите категорию ниже", reply_markup=kb.category_keyboard)

async def app_category(message: Message, state: FSMContext):
    await delete_prev_qna(message)
    await state.update_data(category=message.text)
    await state.set_state(App.time)
    await message.answer("⏰ В какое время с вами связаться?")


async def app_time(message: Message, state: FSMContext):
    await delete_prev_qna(message)
    await state.update_data(time=message.text)
    await state.set_state(App.payment)
    await message.answer("💳 Укажите способ оплаты", reply_markup=kb.payment_keyboard)


async def app_payment(message: Message, state: FSMContext):
    await delete_prev_qna(message)
    await state.update_data(payment=message.text)
    data = await state.get_data()

    user_id = message.from_user.id
    username = message.from_user.username or "не указан"

    application_text = (
        f"✅ Заявка на обучение\n"
        f"👤 От: @{username} (ID:{user_id})\n\n"
        f"📝 Ф.И.О:     {data['name']}\n"
        f"📞 Номер:     {data['phone']}\n"
        f"🏍 Категория: {data['category']}\n"
        f"⏰ Время:     {data['time']}\n"
        f"💳 Оплата:    {data['payment']}"
    )

    await message.answer(application_text, reply_markup=kb.main_page_keyboard)

# Отправляем заявку админу
    try:
        await message.bot.send_message(ADMIN_ID,
                                       f"📥 Новая заявка:\n\n{application_text}",
                                       reply_markup=kb.get_admin_action_keyboard(user_id))
    except Exception as e:
        await message.answer("Не удалось отправить заявку, свяжитесь с Админом в чате")
    await state.clear()

    await message.answer("Спасибо за заявку!", reply_markup=kb.main_page_keyboard)


async def handle_app(message: Message, state: FSMContext):              # (1способ)
    current_state = await state.get_state()
    if current_state == App.name:
        await app_name(message, state)
    elif current_state == App.phone:
        await app_phone(message, state)
    elif current_state == App.category:
        await app_category(message, state)
    elif current_state == App.time:
        await app_time(message, state)
    elif current_state == App.payment:
        await app_payment(message, state)


#----------------------------------
# заявка на вождение


async def drive_name(message: Message, state: FSMContext):
    await delete_prev_qna(message)
    await state.update_data(name=message.text)
    await state.set_state(Drive.d_phone)
    await message.answer("📞 Напишите ваш номер телефона")


async def drive_phone(message: Message, state: FSMContext):
    await delete_prev_qna(message)
    await state.update_data(phone=message.text)
    await state.set_state(Drive.d_stage)
    await message.answer("🧭 У вас есть опыт или вы новичёк?", reply_markup=kb.stage_keyboard)


async def drive_stage(message: Message, state: FSMContext):
    await delete_prev_qna(message)
    await state.update_data(stage=message.text)
    await state.set_state(Drive.d_type_car)
    await message.answer("🚗 Напишите 'механика' или 'автомат'", reply_markup=kb.car_type_keyboard)


async def drive_car(message: Message, state: FSMContext):
    await delete_prev_qna(message)
    await state.update_data(car=message.text)
    await state.set_state(Drive.d_amount)
    await message.answer("✏️ Сколько занятий практики вы хотите?")


async def drive_amount(message: Message, state: FSMContext):
    await delete_prev_qna(message)
    await state.update_data(amount=message.text)
    await state.set_state(Drive.d_time)
    await message.answer("⏰ Предпочтительное время занятий")


async def drive_time(message: Message, state: FSMContext):
    await delete_prev_qna(message)
    await state.update_data(time=message.text)
    data = await state.get_data()

    user_id = message.from_user.id
    username = message.from_user.username or "не указан"

    application_text = (
        f"✅ Заявка на вождение\n"
        f"👤 От: @{username} (ID:{user_id})\n\n"
        f"📝 Ф.И.О:     {data.get('name')}\n"
        f"📞 Телефон:   {data.get('phone')}\n"
        f"🧭 Опыт:      {data.get('stage')}\n"
        f"🚗 Тип авто:  {data.get('car')}\n"
        f"✏️ Занятий:   {data.get('amount')}\n"
        f"⏰ Время:     {data.get('time')}"
    )

    await message.answer(application_text, reply_markup=kb.main_page_keyboard)

# Отправляем заявку админу
    await message.bot.send_message(ADMIN_ID, f"📥 Новая заявка:\n\n{application_text}")

    await state.clear()

    await message.answer("Спасибо за заявку!", reply_markup=kb.main_page_keyboard)


DRIVE_HANDLERS = {                          # (2 способ)
    Drive.d_name: drive_name,
    Drive.d_phone: drive_phone,
    Drive.d_stage: drive_stage,
    Drive.d_type_car: drive_car,
    Drive.d_amount: drive_amount,
    Drive.d_time: drive_time,
}

async def handle_drive(message: Message, state: FSMContext):
    current_state = await state.get_state()
    handler = DRIVE_HANDLERS.get(current_state)
    if handler:
        await handler(message, state)