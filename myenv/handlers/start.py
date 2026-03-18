from aiogram import Router,F
from aiogram.types import Message
from aiogram.filters import CommandStart,Command
from keyboards.reply import register,menyu,admin_menyu
from filters.adminfilter import RoleFilter



router=Router()

@router.message(CommandStart(),RoleFilter('admin'))
async def start_admin(msg:Message):
    await msg.answer(f'Assalomu Alekom {msg.from_user.first_name} ADMIN botimzga yozganingizdan xursandmiz!',reply_markup=admin_menyu())



@router.message(CommandStart())
async def start_handler(msg: Message,db):
    if await db.is_user_exists(msg.from_user.id):
        await msg.answer(f'Assalomu Aleykum {msg.from_user.full_name}, Botimizga yozganingizdan xursandmiz!\nSiz avval royxatdan otgansiz ',reply_markup=menyu())
    else:
        await msg.answer('Assalomu Alekom botga yozganingizdan xursandmiz\nBotimizni qoiadalariga amal qilgan xolda royhatan otishingizni sorayaman: ')
        await msg.answer('Bizning Botimiz toliq siz uchun ishalishi uchun REGISTRATsiyadan otin',reply_markup=register())
        
        
