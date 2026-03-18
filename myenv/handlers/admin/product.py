from aiogram import F,Router
from aiogram.types import Message
from filters.adminfilter import RoleFilter
from aiogram.fsm.context import FSMContext
from states.add_product.product_add import AddPro

router=Router()

@router.message(F.text=="Mahsulotlar qoshish",RoleFilter('admin'))
async def add_product(msg:Message,state:FSMContext):
    await msg.answer("Mahsulotni qo'shish uchun iltimos mahsulot nomini yozing: ")
    await state.set_state(AddPro.name)

@router.message(AddPro.name)
async def add_product(msg:Message,state:FSMContext):
    await state.update_data(name=msg.text)
    await msg.answer("mahsulot narxini yozing: ")
    await state.set_state(AddPro.price)
    
@router.message(AddPro.price)
async def add_product(msg:Message,state:FSMContext):
    await state.update_data(price=int(msg.text))
    await msg.answer("mahsulot description yozing: ")
    await state.set_state(AddPro.description)

@router.message(AddPro.description)
async def add_product(msg:Message,state:FSMContext,db):
    await state.update_data(description=msg.text)

    data=await state.get_data()

    await db.add_product(data["name"],data["price"],data["description"])
    await msg.answer("Mahsulot muvaffaqiyatli qo'shildi")
    await state.clear()