from aiogram import Router,F
from aiogram.types import Message,CallbackQuery
from filters.adminfilter import RoleFilter
from keyboards.inline import savat_inline
router=Router()

@router.callback_query(F.data.startswith("product_"),RoleFilter('user'))
async def product(call:CallbackQuery,db):
    product_id= int(call.data.split("_")[1])
    user_id= await db.get_user_id(call.from_user.id)
    await db.add_product_to_cart(user_id,product_id)
    await call.answer("Mahsulot savatga qo'shildi")

@router.message(F.text=="Savatcha")
async def savatcha(msg:Message,db):
    user_id= await db.get_user_id(msg.from_user.id)
    products=await db.get_cart_products(user_id)
    await msg.answer("Mahsulotlar ro'yxati: ",reply_markup=savat_inline(products))