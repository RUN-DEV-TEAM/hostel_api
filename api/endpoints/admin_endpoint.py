from fastapi import APIRouter,Depends, Body, Query, HTTPException
from typing import List
from schemas.userSchema import CreateUser,ReturnSignUpUser,ListUser
from schemas.blockSchemas import BlockSchema
from dependencies import get_session
from services import admin_service
from api.endpoints.endpoint_helper import  get_current_user
from sqlalchemy.ext.asyncio import async_sessionmaker
from fastapi.responses import JSONResponse


router = APIRouter()

@router.post("/sign_up",response_model=ReturnSignUpUser)
async def sign_up(user: CreateUser, session: async_sessionmaker = Depends(get_session)):
  return await admin_service.sign_up_service(user,session)


@router.get("/list_users", response_model=List[ReturnSignUpUser])
async def list_users(session: async_sessionmaker = Depends(get_session), user: ReturnSignUpUser =Depends(get_current_user)):
  return await admin_service.list_user_service(session)


# 
@router.get("/get_user_by_email", response_model=ListUser)
async def get_user(email:str, session: async_sessionmaker = Depends(get_session), user: ReturnSignUpUser =Depends(get_current_user)):
  res =  await admin_service.get_user_by_email_service(email, session)
  if not res:
    return JSONResponse(status_code=404, content={"message": "User not found"})     
  return res


@router.post("/create_block")
async def create_new_block(block_input:BlockSchema,session: async_sessionmaker = Depends(get_session)):
  res = await admin_service.create_new_block_db_service(block_input,session)
  if "error" in res:
    return JSONResponse(status_code=404, content={"message": res})  
  return res 