from api.endpoints.endpoint_helper import  get_current_user
from sqlalchemy.ext.asyncio import async_sessionmaker
from fastapi.responses import JSONResponse
from dependencies import get_session
from fastapi import APIRouter,Depends
from typing import List
from schemas.userSchema import ReturnSignUpUser

router = APIRouter()

# param: matric number
@router.get("/assign_room_to_student_in_session")
async def assign_room_to_student_in_session_func(block_id:int, session: async_sessionmaker = Depends(get_session), user: ReturnSignUpUser =Depends(get_current_user)):
  pass
