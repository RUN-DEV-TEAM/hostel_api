from sqlalchemy.ext.asyncio import  create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
import os
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
from models import *


engine = create_async_engine(os.getenv("DATABASE_URL"), echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False )

async def init_db():
    async with engine.begin() as conn:
        #  await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all) 
    # for AsyncEngine created in function scope, close and
    # clean-up pooled connections
    await engine.dispose()




