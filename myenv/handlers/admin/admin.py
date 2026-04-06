from aiogram import Router,F
from aiogram.types import Message
from keyboards.reply import admin_panel,admin_menyu
from keyboards.inline import users_inline,user_action
from filters.adminfilter import RoleFilter
from states.AddState import Reklama
from aiogram.fsm.context import FSMContext

router=Router()

@router.message(F.text=='Admin panel',RoleFilter('admin'))
async def admin_(msg:Message):
    await msg.answer(f'Admin panelga otildi!',reply_markup=admin_panel())
    

@router.message(F.text=='Users', RoleFilter('admin'))
async def user(msg:Message, db):
    users = await db.get_users()
    print("DB natijasi:", users)
    await msg.answer("Foydalanuvchilar ro'yxati", reply_markup=users_inline(users))
    
    
from aiogram.types import CallbackQuery

@router.callback_query(F.data.startswith("user_"))
async def select_user(call: CallbackQuery):
    user_id = call.data.split("_")[1]

    await call.message.answer(
        "User rolini tanlang:",
        reply_markup=user_action(user_id)
    )
    await call.answer('Ozgardi')
    
@router.callback_query(F.data.startswith("changeto_"))
async def user(call:CallbackQuery,db):
    _,role,user_id=call.data.split("_")
    user_id=int(user_id)
    await db.update_role(user_id,role)
    await call.message.answer('ROEL ozgardi ADMIN')
    await call.answer()
    
@router.message(F.text=='Orqaga')
async def orqa(msg:Message):
    await msg.answer("Orqaga qaytildi👇",reply_markup=admin_menyu())
    

    
@router.message(F.text.lower() == "Reklama", RoleFilter("admin"))
async def reklama(msg: Message, state: FSMContext):
    await msg.answer("📢 Reklama yuborish uchun rasm, video yoki matn yuboring:")
    await state.set_state(Reklama.waiting_for_ads)


@router.message(Reklama.waiting_for_ads)
async def reklama_send(msg: Message, state: FSMContext, db):
    users = await db.get_users_telegram_id()

    success, failed = 0, 0

    for user in users:
        try:
            
            if msg.photo:
                await msg.bot.send_photo(
                    chat_id=int(user),
                    photo=msg.photo[-1].file_id,
                    caption=msg.caption
                )

            
            elif msg.video:
                await msg.bot.send_video(
                    chat_id=int(user),
                    video=msg.video.file_id,
                    caption=msg.caption
                )

            
            elif msg.text:
                await msg.bot.send_message(
                    chat_id=int(user),
                    text=msg.text
                )

            success += 1

        except Exception as e:
            failed += 1
            print(f"Xatolik: {e}")

    await msg.answer(
        f"✅ Yuborildi: {success} ta\n❌ Yuborilmadi: {failed} ta"
    )

    await state.clear()
