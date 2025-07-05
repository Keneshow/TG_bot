from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton




main_page_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [
            types.KeyboardButton(text="Заявки"),
            types.KeyboardButton(text="Вождение")

        ],
    ],
    resize_keyboard = True
)


category_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text="A"),
         types.KeyboardButton(text="B"),
         types.KeyboardButton(text="C")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)


car_type_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text="механика"),
         types.KeyboardButton(text="автомат")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)


stage_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text="Да бывало водил"),
         types.KeyboardButton(text="Я новичёк")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)


payment_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text="Наличными"),
         types.KeyboardButton(text="Переводом")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)


def get_contact_and_location_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Чат с админом",
                                 url="https://t.me/Keneshow_93")
        ],
        [
            InlineKeyboardButton(text="Открыть адрес в 2ГИС",
                                 url="https://2gis.kg/bishkek/firm/70000001059573568?m=74.503291%2C42.874808%2F16")
        ],
        [
            InlineKeyboardButton(
                text="Прайс и время обучения",
                callback_data="show_price"
            )
        ]
    ])


def get_admin_action_keyboard(user_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Обработано", callback_data=f"processed_{user_id}"),
            InlineKeyboardButton(text="🗑 Удалить", callback_data=f"delete_{user_id}"),
            InlineKeyboardButton(text="📤 Ответить", callback_data=f"reply_{user_id}")
        ]
    ])