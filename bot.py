from aiogram import Bot,Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from database.db import Database
import asyncio


from handlers.start import router as start_router
from handlers.register import router as register_router
from handlers.users.profile import router as profile_router
from handlers.admin.admin import router as admin_router
from handlers.products.product import router as product_router
from handlers.admin.product import router as admin_product
from handlers.users.products import router as users_products_router




async def main():
    bot=Bot(token='8715422053:AAFF6Kzzo3Tx1kquJooB3v153nCvPV9zOkA')
    storage = MemoryStorage()
    dp=Dispatcher(storage=storage)
    
    db = Database()
    await db.connect()
    dp['db']=db

    
    
    dp.include_router(start_router)
    dp.include_router(register_router)
    dp.include_router(profile_router)
    dp.include_router(admin_router)
    dp.include_router(product_router)
    dp.include_router(admin_product)
    dp.include_router(users_products_router)
    



    await dp.start_polling(bot)
if __name__=="__main__":
    print('Bot is started😎')
    asyncio.run(main())