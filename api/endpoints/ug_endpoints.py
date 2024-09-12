from api.endpoints.endpoint_helper import  get_current_user,require_permission
from sqlalchemy.ext.asyncio import async_sessionmaker
from fastapi.responses import JSONResponse
from dependencies import get_session
from fastapi import APIRouter,Depends
from typing import List
from schemas.userSchema import ReturnSignUpUser
from schemas.helperSchema import UserType
from services import admin_service, student_service

router = APIRouter()

@router.post("/allocate_room_to_student_in_session",response_model="")
async def allocate_room_to_student_in_session_func(mat_no:str, session: async_sessionmaker = Depends(get_session), user: ReturnSignUpUser =Depends(require_permission(UserType.ADMIN))):
  res = await student_service.get_student_profile_and_allocate_room_to_the_student_service(mat_no,session)
  if not res[0]:
    return JSONResponse(status_code=404, content=res[1])  
  elif res[0]:
    return res[1] #JSONResponse(status_code=200, content={}) 


@router.post("/get_student_room_in_session",response_model="")
async def get_student_room_in_session_func(mat_no:str, session_id:str, session: async_sessionmaker = Depends(get_session), user: ReturnSignUpUser =Depends(get_current_user)):
  res = await admin_service.get_student_room_in_session_service(mat_no, session_id,session)
  if not res[0]:
    return JSONResponse(status_code=404, content=res[1]) 
  elif res[0]:
    return res[1]
  


@router.post("/get_available_space_from_guest_house",response_model="")
async def get_available_space_from_guest_house_func(session: async_sessionmaker = Depends(get_session), user: ReturnSignUpUser =Depends(get_current_user)):
  res = await admin_service.get_available_space_from_guest_house_service(session)
  if not res[0]:
    return JSONResponse(status_code=404, content=res[1]) 
  elif res[0]:
    return res[1]