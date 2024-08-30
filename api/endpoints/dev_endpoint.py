from api.endpoints.endpoint_helper import  get_current_user
from sqlalchemy.future import select
from sqlalchemy import func,distinct
from sqlalchemy.ext.asyncio import async_sessionmaker
from fastapi.responses import JSONResponse
from dependencies import get_session
from fastapi import APIRouter,Depends
from typing import List
from schemas.userSchema import ReturnSignUpUser
from services import admin_service, student_service
from models.studentModel import *
from models.userModel import *
router = APIRouter()


# , user: ReturnSignUpUser =Depends(get_current_user)
@router.post("/test_queries")
async def test_queries(session: async_sessionmaker = Depends(get_session)):
    query = await session.execute(
        select(BlockModel.id,BlockModel.block_name,BlockModel.gender).where(BlockModel.block_status=="AVAILABLE")
        .where(BlockModel.id.in_(select(BlockProximityToFacultyModel.block_id).where(BlockProximityToFacultyModel.faculty ==4))))
    # res = query.scalars().all()
    res = query.all()
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print(type(res))
    print(res)
    print(len(res))
    
    
    return {"message":"Testing"}