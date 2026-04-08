from aiogram import Router,F
from aiogram.types import Message

router=Router()

@router.message(F.text=='Profile')
async def profile(msg:Message,db):
    tg_id=msg.from_user.id
    data=await db.profi(tg_id)
    await msg.answer(f"Sizning ma'lumotlaringiz")
    
    await msg.answer(
        f"Sizning ma'lumotlaringiz:\n"
        f"Ism: {data['name']}\n"
        f"Familya: {data['surname']}\n"
        f"Yosh: {data['age']}\n"
        f"Telefon Nomer: {data['phone_number']}\n"
        f"Mansab: {data['role']}"
    )