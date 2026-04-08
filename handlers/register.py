from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states.register import RegisterState
from keyboards.reply import menyu, contact

router = Router()

@router.message(F.text == 'Register')
async def register_handler(msg: Message, state: FSMContext, db):
    if await db.is_user_exists(msg.from_user.id):
        await msg.answer(
            "Siz avval ro'yxatdan o'tgansiz!\nIltimos menyudan foydalaning",
            reply_markup=menyu()
        )
        return

    await msg.answer("Registratsiyadan o‘tish uchun ismingizni yozing:")
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
async def process_age(msg: Message, state: FSMContext):
    try:
        age = int(msg.text)
    except ValueError:
        await msg.answer("Iltimos, yoshni raqam bilan kiriting:")
        return

    await state.update_data(age=age)

    await msg.answer(
        "Telefon raqamingizni yuboring:",
        reply_markup=contact()
    )
    await state.set_state(RegisterState.contact)



@router.message(RegisterState.contact, F.contact)
async def process_phone(msg: Message, state: FSMContext, db):
    phone = msg.contact.phone_number


    if msg.contact.user_id != msg.from_user.id:
        await msg.answer("Iltimos, o'zingizning raqamingizni yuboring!")
        return

    await state.update_data(contact=phone)

    data = await state.get_data()

    await msg.answer(
        f"Ism: {data['name']}\n"
        f"Familya: {data['surname']}\n"
        f"Yosh: {data['age']}\n"
        f"Telefon: {data['contact']}"
    )

    await db.add_user(
        int(msg.from_user.id),
        data['name'],
        data['surname'],
        data['age'],
        data['contact']
    )

    await msg.answer("✅ Registratsiya muvaffaqiyatli yakunlandi!",reply_markup=menyu())
    await state.clear()