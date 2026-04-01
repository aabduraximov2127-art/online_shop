from aiogram.types import ReplyKeyboardMarkup,KeyboardButton


def register():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Register")]
        ],
        resize_keyboard=True
    )

def menyu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Mahsulotlar"),KeyboardButton(text='Mening Buyurtmalarim')],
            [KeyboardButton(text='Profile'),KeyboardButton(text='Savatcha')]
        ],
        resize_keyboard=True
    )

def admin_menyu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Mahsulotlar"),KeyboardButton(text='Mening Buyurtmalarim')],
            [KeyboardButton(text='Profile'),KeyboardButton(text='Admin panel')]
        ],
        resize_keyboard=True
    )


def admin_panel():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Mahsulotlar qoshish"),KeyboardButton(text='Buyurtmalar')],
            [KeyboardButton(text='Users'),KeyboardButton(text='Orqaga')]
        ],
        resize_keyboard=True
    )