from aiogram import Router,F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states.register import RegisterState
from keyboards.reply import menyu


router=Router()


@router.message(F.text == 'Register',)
async def register_handler(msg: Message, state: FSMContext,db):
    if await db.is_user_exists(msg.from_user.id):
        await msg.answer('Siz avval royhardan otib bolgan ekansiz!\nIltoms asosiy menyudan foydalaning',reply_markup=menyu())
    else:  
        await msg.answer('Registratsiyadan o‘tish uchun ismingizni yozing:')
    await state.set_state(RegisterState.name)


@router.message(RegisterState.name)
async def get_name(msg: Message, state: FSMContext):
    await state.update_data(name=msg.text)
    await msg.answer("Familyangizni kiriting:")
    await state.set_state(RegisterState.surname)


@router.message(RegisterState.surname)
async def get_surname(msg: Message, state: FSMContext):
    await state.update_data(surname=msg.text)
    await msg.answer("Yoshingizni kiriting:")
    await state.set_state(RegisterState.age)


@router.message(RegisterState.age)
async def process_age(msg:Message, state: FSMContext):

    try:
        age = int(msg.text)
    except ValueError:
        await msg.answer("Iltimos, raqam bilan yozing:")
        return
    await state.update_data(age=age)
    await msg.answer("Telefon raqamingizni yozing:")
    await state.set_state(RegisterState.phone_number)


@router.message(RegisterState.phone_number)
async def process_phone(msg: Message, state: FSMContext, db):
    await state.update_data(phone_number=msg.text)
    
    data=await state.get_data()
    await msg.answer(f"Ism:{data['name']}\nFamilya: {data['surname']}\nYosh: {data['age']}\nTelefon Nomer: {data['phone_number']} ")
    await db.add_user(int(msg.from_user.id),data['name'],data['surname'],data['age'],data['phone_number'])
    await msg.answer("Ma'lumotlaringiz qabul qilindi va Siz Registratsiyadan muvaffaqiyatli o'tdingiz!")
    await state.clear()