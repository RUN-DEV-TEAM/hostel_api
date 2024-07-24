from api.endpoints.endpoint_helper import  get_current_user
from sqlalchemy.ext.asyncio import async_sessionmaker
from fastapi.responses import JSONResponse
from schemas.userSchema import ReturnSignUpUser
from dependencies import get_session
from fastapi import APIRouter,Depends
from typing import List


router = APIRouter()

@router.post("/allocate_room_to_student_in_session",response_model="")
async def allocate_room_to_student_in_session_func(student, session: async_sessionmaker = Depends(get_session), user: ReturnSignUpUser =Depends(get_current_user)):
    pass