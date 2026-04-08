from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from filters.adminfilter import RoleFilter
from keyboards.inline import savat_inline, payment_keyboard
from keyboards.reply import pul_tushti,menyu

router = Router()

ADMIN_ID = 7997652702



@router.callback_query(F.data.startswith("product_"), RoleFilter('user'))
async def add_to_cart(call: CallbackQuery, db):
    product_id = int(call.data.split("_")[1])
    user_id = await db.get_user_id(call.from_user.id)

    await db.add_product_to_cart(user_id, product_id)

    await call.answer("✅ Mahsulot savatga qo‘shildi")



@router.message(F.text == "Savatcha")
async def show_cart(msg: Message, db):
    user_id = await db.get_user_id(msg.from_user.id)
    products = await db.get_cart_products(user_id)

    if not products:
        await msg.answer("🛒 Savatchangiz bo‘sh")
        return

    await msg.answer(
        "🛒 Savatchangizdagi mahsulotlar:",
        reply_markup=savat_inline(products)
    )



@router.callback_query(F.data.startswith("remove_product_"))
async def remove_from_cart(call: CallbackQuery, db):
    user_id = await db.get_user_id(call.from_user.id)
    product_id = int(call.data.split("_")[2])

    await db.remove_one_product(user_id, product_id)

    products = await db.get_cart_products(user_id)

    if not products:
        await call.message.answer("🛒 Savatchangiz bo‘sh")
    else:
        await call.message.answer(
            "🛒 Yangilangan savat:",
            reply_markup=savat_inline(products)
        )

    await call.answer("❌ Mahsulot o‘chirildi")



@router.callback_query(F.data == 'order')
async def make_order(call: CallbackQuery, db):
    user_id = await db.get_user_id(call.from_user.id)
    products, total = await db.get_cart_with_total(user_id)

    await call.answer()

    if not products:
        await call.message.answer("🛒 Savatchangiz bo‘sh")
        return

    text = "🛒 <b>Buyurtma:</b>\n\n"

    for product in products:
        text += f"• {product['name']} — {product['price']} so‘m\n"

    text += f"\n💰 <b>Jami:</b> {total} so‘m"


    await call.message.answer(
        text,
        reply_markup=payment_keyboard(),
        parse_mode="HTML"
    )


    await call.bot.send_message(
        ADMIN_ID,
        "🆕 <b>Yangi buyurtma!</b>\n\n" + text,
        parse_mode="HTML"
    )



@router.callback_query(F.data.startswith("naxt"))
async def cash_payment(call: CallbackQuery):
    await call.message.answer("❌ Hozircha naqd to‘lov mavjud emas")
    await call.answer()



@router.callback_query(F.data == "karta")
async def card_payment(call: CallbackQuery,db):
    await call.message.answer(
        "💳 <b>Karta orqali to‘lov</b>\n\n"
        "Quyidagi kartaga to‘lov qiling:\n"
        "<code>9860 6004 1234 1234</code>\n"
        "👤 User\n\n"
        "To‘lov qilgandan keyin <b>'Tushdi'</b> deb yozing 👇",
        reply_markup=pul_tushti(),
        parse_mode="HTML"
    )
    user_id=await db.get_user_id(call.from_user.id)
    await db.confirm_order(user_id)
    await call.answer()



@router.message(F.text.lower() == 'tushdi')
async def payment_confirm(msg: Message):
    await msg.answer(
        "✅ To‘lovingiz tekshirildi!\n"
        "📦 Buyurtmangiz tez orada yetkaziladi.\n\n"
        "🙏 Raxmat!",reply_markup=menyu()
    )
    
@router.message(F.text == 'Mening Buyurtmalarim')
async def history(msg: Message, db):
    user_id = await db.get_user_id(msg.from_user.id)
    orders = await db.get_user_order_history(user_id)

    if not orders:
        await msg.answer("📭 Sizda buyurtmalar yo'q")
        return

    for order_id, data in orders.items():
        text = f"📦 Buyurtma #{order_id}\n"

        for p in data['products']:
            name = p["name"]
            price = p["price"]
            text += f"- {name} ({price} so'm)\n"

        text += f"\n💰 Jami: {data['total']} so'm"

        await msg.answer(text)
        
        
@router.callback_query(F.data=='order')
async def card_payment(call: CallbackQuery, db):
    user_id = await db.get_user_id(call.from_user.id)
    
    
    await db.confirm_order(user_id)
    

    await call.message.answer("✅ Buyurtmangiz qabul qilindi! Savatchangiz bo‘shatildi.")
    

@router.callback_query(lambda c: c.data == "clear_cart")
async def clear_cart_handler(call: CallbackQuery,db):


    user_id = call.from_user.id

    await db.clear_cart(user_id)

    
    await call.message.edit_text("🛒 Savatchangiz bo'shatildi", reply_markup=savat_inline([]))
    await call.answer()