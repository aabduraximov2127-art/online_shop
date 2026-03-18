from aiogram import Router,F
from aiogram.types import Message
from keyboards.inline import inline_product

router=Router()


@router.message(F.text == "Mahsulotlar")
async def prod(msg: Message, db):
    products = await db.get_products()

    await msg.answer(
        "Mahsulotlar ro'yxati:",
        reply_markup=inline_product(products)  
    )