from fastapi import APIRouter,Depends, HTTPException, status
from dependencies import get_session
from api.endpoints import endpoint_helper
from sqlalchemy.ext.asyncio import async_sessionmaker
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from schemas.userSchema import Token,ReturnSignUpUser,CreateUser
from services import admin_service
router = APIRouter()


@router.post("/sign_up",response_model=ReturnSignUpUser)
async def sign_up(user: CreateUser, session: async_sessionmaker = Depends(get_session)):
  service_resp = await admin_service.sign_up_service(user,session)
  if not service_resp[0]:
    return JSONResponse(status_code=404, content=service_resp[1])
  elif service_resp[0]:
    return service_resp[1]


# AUTH START
# pip install python-jose[cryptography] pip install passlib[bcrypt]  
# run "openssl rand -hex 32"  to generate SECRET_KEY
@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),  session: async_sessionmaker = Depends(get_session)):
    user = await endpoint_helper.authenticate_user(form_data.username, form_data.password, session)
    if not user[0]:
            return JSONResponse(status_code=404, content=user[1]) 
    return {"access_token": user[1]["token"], "token_type": "bearer"}
