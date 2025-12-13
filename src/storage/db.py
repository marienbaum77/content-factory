from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from pydantic_settings import BaseSettings, SettingsConfigDict

class DbSettings(BaseSettings):
    db_host: str
    db_port: int
    db_user: str
    db_pass: str
    db_name: str
    
    # ВОТ ИСПРАВЛЕНИЕ: добавляем extra="ignore"
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore" 
    )

config = DbSettings()

DATABASE_URL = f"postgresql+asyncpg://{config.db_user}:{config.db_pass}@{config.db_host}:{config.db_port}/{config.db_name}"

engine = create_async_engine(DATABASE_URL, echo=False)

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)