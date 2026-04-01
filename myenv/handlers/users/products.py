from aiogram import Router,F
from aiogram.types import Message,CallbackQuery
from filters.adminfilter import RoleFilter
from keyboards.inline import savat_inline,payment_keyboard
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
    
@router.callback_query(F.data.startswith("remove_product_"))
async def remove_from_cart(call:CallbackQuery,db):
    user_id= await db.get_user_id(call.from_user.id)
    product_id= int(call.data.split("_")[2])
    await db.remove_one_product(user_id,product_id)
    products=await db.get_cart_products(user_id)
    await call.message.answer("Mahsulotlar ro'yxati: ",reply_markup=savat_inline(products))
    await call.answer()

@router.callback_query(F.data=='order')
async def zakaz(call:CallbackQuery,db):
    user_id= await db.get_user_id(call.from_user.id)
    products,total=await db.get_cart_with_total(user_id)
    await call.answer()
    if not products:
        await call.message.answer("Savatchangiz bo'sh")
        return

    text = "🛒 Buyurtmalar:\n\n"

    for product in products:
        text += f"• {product['name']} - {product['price']} so'm\n"

    text += f"\n💰 Obwiy narx: {total} so'm"

    await call.message.answer(
        text,
        reply_markup=payment_keyboard()
    )
    
@router.callback_query(F.data.startswith("karta"))
async def karta_tolov(call:CallbackQuery):
    await call.message.answer("Kartadan tolov Mana shu kartaga obshiy summani va chekini yuboring👇\nKarta raqami👉: 1234 1234 1234 1234💳\nIsm Familya:👉:User user ")
    await call.answer()
    
@router.callback_query(F.data.startswith("naxt"))
async def naxt_tolov(call:CallbackQuery):
    await call.message.answer("Uzur xozir naxt tolovimiz yoq!😫\nSababi bizni yetkazib berish xizmatimiz vaqtinchalik ishlamayapti\nYetkazib berish xizmatim ishga tushishi bilan 💵Naxt tolov qilsa boladi!")
    await call.answer()
