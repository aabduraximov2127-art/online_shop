import asyncpg
from config import config


class Database:
    def __init__(self):
        self.pool=None
        
        
    async def connect(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            database=config.DB_NAME,
            host=config.DB_HOST,
            port=config.DB_PORT
        )
        print("✅ Database connected")

            
    
    async def add_user(self,telegram_id,name,surname,age,phone_number):
        query="""
        insert into users(name,surname,age,phone_number,telegram_id) values($1,$2,$3,$4,$5)
        """
        await self.pool.execute(query,name,
        surname,age,phone_number,telegram_id)
        
    
    async def is_user_exists(self, telegram_id: int) -> bool:
        query = """
        SELECT EXISTS (
        SELECT 1 FROM users WHERE telegram_id = $1
        );
        """
        return await self.pool.fetchval(query, telegram_id)
    
    
    async def profi(self, tg_id):
        query = """
        SELECT telegram_id, name, surname, age, phone_number,
        role
        FROM users
        WHERE telegram_id = $1
        """
        return await self.pool.fetchrow(query, tg_id)
    
    
    async def get_user_role(self,telegram_id):
        query="""SELECT role FROM users where telegram_id=$1
        """
        return await self.pool.fetchval(query,telegram_id)
    
    async def get_users(self):
        query="""
        select name,surname,role,id from users order by id;
        """
        return await self.pool.fetch(query)
    
    async def update_role(self,user_id,role):
        query="""
        update users set role=$1 where id=$2
        """
        await self.pool.execute(query,role,user_id)
        
    # products
    
    async def get_products(self):
        query="""
        select id,name,price from products order by id
        """
        return await self.pool.fetch(query)
    
    
    async def add_product(self,name,price,description):
        query="""
        insert into products(name,price,description) values($1,$2,$3);
        """

        await self.pool.execute(query,name,price,description)