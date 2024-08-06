from fastapi import APIRouter,Depends, Body, Query, HTTPException
from typing import List
from schemas.userSchema import CreateUser,ReturnSignUpUser,ListUser
from schemas.blockSchemas import BlockSchema,BlockRoomSchema,GetRoomStat
from schemas.helperSchema import Gender
from dependencies import get_session
from services import admin_service
from api.endpoints.endpoint_helper import  get_current_user
from sqlalchemy.ext.asyncio import async_sessionmaker
from fastapi.responses import JSONResponse


router = APIRouter()


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


@router.post("/create_block", response_model=BlockRoomSchema)
async def create_new_block(block_input:BlockSchema,session: async_sessionmaker = Depends(get_session), user: ReturnSignUpUser =Depends(get_current_user)):
  res = await admin_service.create_new_block_db_service(block_input,session)
  if not res[0]:
    return JSONResponse(status_code=404, content={"message": res[1]})  
  elif res[0]:
    return res[1]

@router.put("/update_block", response_model=BlockRoomSchema)
async def update_block(block_id:int ,block_input:BlockSchema,session: async_sessionmaker = Depends(get_session), user: ReturnSignUpUser =Depends(get_current_user)):
  pass


@router.get("/get_rooms_stat", response_model=GetRoomStat)
async def get_rooms_stat(session: async_sessionmaker = Depends(get_session), user: ReturnSignUpUser =Depends(get_current_user)):
  res = await admin_service.get_rooms_stat_service(session)
  if not res[0]:
    return JSONResponse(status_code=404, content={"message": res[1]})  
  elif res[0]:
    return res[1]
  


@router.get("/get_all_available_rooms_from_selected_block", response_model='')
async def get_all_available_rooms_from_selected_block(block_id:int, session: async_sessionmaker = Depends(get_session), user: ReturnSignUpUser =Depends(get_current_user)):
  res = await admin_service.get_all_available_rooms_from_selected_block_service(block_id,session)
  if not res[0]:
    return JSONResponse(status_code=404, content={"message": res[1]})  
  elif res[0]:
    return res[1]


# 

@router.get("/get_all_occupied_rooms_from_selected_block", response_model='')
async def get_all_occupied_rooms_from_selected_block_service(block_id:int, session: async_sessionmaker = Depends(get_session), user: ReturnSignUpUser =Depends(get_current_user)):
  res = await admin_service.get_all_occupied_rooms_from_selected_block_service(block_id,session)
  if not res[0]:
    return JSONResponse(status_code=404, content={"message": res[1]})  
  elif res[0]:
    return res[1]


# param: matric number
@router.post("/random_assign_room_to_student_in_session")
async def random_assign_room_to_student_in_session_func(mat_no:str,gender:Gender, session: async_sessionmaker = Depends(get_session), user: ReturnSignUpUser =Depends(get_current_user)):
  res = await admin_service.random_assign_room_to_student_in_session_service(mat_no,gender,session)
  if not res[0]:
    return JSONResponse(status_code=404, content={"message": res[1]})  
  elif res[0]:
    return res[1]
  


# param: matric number
@router.post("/assign_room_in_specific_block_to_student_in_session")
async def assign_room_in_specific_block_to_student_in_session_func(mat_no:str,gender:Gender,block_id:int, session: async_sessionmaker = Depends(get_session), user: ReturnSignUpUser =Depends(get_current_user)):
  res = await admin_service.assign_room_in_specific_block_to_student_in_session_service(mat_no,gender,block_id,session)
  if not res[0]:
    return JSONResponse(status_code=404, content={"message": res[1]})  
  elif res[0]:
    return res[1]


# param: matric number
@router.post("/assign_specific_space_in_room_to_student_in_session")
async def assign_specific_space_in_room_to_student_in_session_func(mat_no:str,gender:Gender,room_id:int, session: async_sessionmaker = Depends(get_session), user: ReturnSignUpUser =Depends(get_current_user)):
  res = await admin_service.assign_specific_space_in_room_to_student_in_session_service(mat_no,gender,room_id,session)
  if not res[0]:
    return JSONResponse(status_code=404, content={"message": res[1]})  
  elif res[0]:
    return res[1]


# param: matric number
@router.get("/get_student_room_in_session")
async def get_student_room_in_session_func(mat_no:str,session_id:str, session: async_sessionmaker = Depends(get_session), user: ReturnSignUpUser =Depends(get_current_user)):
  res = await admin_service.get_student_room_in_session_service(mat_no, session_id,session)
  if not res[0]:
    return JSONResponse(status_code=404, content={"message": res[1]}) 
  elif res[0]:
    return res[1]


# param: matric number
@router.delete("/delete_student_from_room_in_session",description="Just a soft delete")
async def delete_student_from_room_in_session_func(block_id:int, session: async_sessionmaker = Depends(get_session), user: ReturnSignUpUser =Depends(get_current_user)):
  pass

# param: matric number
@router.put("/change_student_room_in_session")
async def change_student_room_in_session_func(block_id:int, session: async_sessionmaker = Depends(get_session), user: ReturnSignUpUser =Depends(get_current_user)):
  pass

@router.get("/list_students_in_room_in_session")
async def list_student_in_room_in_session_func( session: async_sessionmaker = Depends(get_session), user: ReturnSignUpUser =Depends(get_current_user)):
  pass


@router.get("/get_room_status_in_session")
async def get_room_status_in_session_func( session: async_sessionmaker = Depends(get_session), user: ReturnSignUpUser =Depends(get_current_user)):
  pass

@router.put("/update_room_status_in_session")
async def update_room_status_in_session_func( session: async_sessionmaker = Depends(get_session), user: ReturnSignUpUser =Depends(get_current_user)):
  pass

@router.get("/list_rooms_with_empty_space_in_session")
async def list_rooms_with_empty_space_in_session_func( session: async_sessionmaker = Depends(get_session), user: ReturnSignUpUser =Depends(get_current_user)):
  pass

@router.get("/list_occupied_rooms_in_session")
async def list_occupied_rooms_in_session_func( session: async_sessionmaker = Depends(get_session), user: ReturnSignUpUser =Depends(get_current_user)):
  pass


@router.get("/list_blocks_with_empty_rooms_in_session")
async def list_blocks_with_empty_rooms_in_session_func( session: async_sessionmaker = Depends(get_session), user: ReturnSignUpUser =Depends(get_current_user)):
  pass

@router.get("/list_students_in_block_in_session")
async def list_students_with_accomodation_in_block_in_session_func(block_id:int, session: async_sessionmaker = Depends(get_session), user: ReturnSignUpUser =Depends(get_current_user)):
  pass

@router.get("/list_students_with_accomodation_in_session")
async def list_students_with_accomodation_in_session_func( session: async_sessionmaker = Depends(get_session), user: ReturnSignUpUser =Depends(get_current_user)):
  pass
    # $students =   DB::table('t_students')->select('matric_number',
  #           DB::raw("CONCAT(t_students.surname,' ',t_students.firstname,' ',t_students.othernames) as full_name"),
  #           'sex','current_level','student_phone','picture',$param2 )
  #            ->where('sex',$sex)
  #           ->where('room_no','like',$param)->get();
  #             return response()->json(['status'=>'ok', 'msg' =>'success', 'data'=> $students,'session'=>$cur_session]);


