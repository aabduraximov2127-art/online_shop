from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def users_inline(users):
    keyboard = []
    
    for user in users:
        keyboard.append([
            InlineKeyboardButton(
                text=f"{user['name']} {user['surname']} {user['role']}",
                callback_data=f"user_{user['id']}"
            )
        ])
    

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def user_action(user_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='admin',callback_data=f"changeto_admin_{user_id}"),InlineKeyboardButton(text='user',callback_data=f'changeto_user_{user_id}')]
        ]
    )

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def inline_product(products):
    keyboard = []
    
    for product in products:
        keyboard.append([
            InlineKeyboardButton(
                text=f"{product['name']} - {product['price']} so'm",
                callback_data=f"product_{product['id']}"
            )
        ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def product_action(product_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Edit",callback_data=f"edit_product_{product_id}"),InlineKeyboardButton(text="Delete",callback_data=f"delete_product_{product_id}")]
        ]
    )
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def savat_inline(products):
    keyboard = []

    for product in products:
        keyboard.append([
            InlineKeyboardButton(
                text=f"{product['name']} ({product['price']} so'm)",
                callback_data="1"
            ),
            InlineKeyboardButton(
                text="❌",
                callback_data=f"remove_product_{product['id']}"
            )
        ])
    
    keyboard.append([
        InlineKeyboardButton(
            text="Buyurtma berish",
            callback_data="order"
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def payment_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(
                text="Kartadan Tolov 💳",
                callback_data="karta"
            )
        ],
        [
            InlineKeyboardButton(
                text="Naqd Tolov 💵",
                callback_data="naxt"
            )
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
