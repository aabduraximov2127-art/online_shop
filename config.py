from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()

@dataclass
class Config:
    BOT_TOKEN: str=os.getenv("BOT_TOKEN")


    DB_HOST: str = os.getenv("DB_HOST", "localhost")        
    DB_PORT: int = int(os.getenv("DB_PORT", 5432))         
    DB_NAME: str = os.getenv("DB_NAME", "online_shop")    
    DB_USER: str = os.getenv("DB_USER", "postgres")        
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "1234") 


    
    
config=Config()