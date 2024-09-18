from api.endpoints.endpoint_helper import  get_current_user
from sqlalchemy.future import select
from sqlalchemy import func,distinct,update, and_,delete, or_
from sqlalchemy.ext.asyncio import async_sessionmaker
from fastapi.responses import JSONResponse
from dependencies import get_session
from fastapi import APIRouter,Depends
from typing import List
from schemas.userSchema import ReturnSignUpUser
from services import admin_service, student_service
from models.studentModel import *
from models.userModel import *
from schemas.blockSchemas import BlockSchemaCreate
import random
import asyncio
router = APIRouter()



# ==: Equal to
# !=: Not equal to
# <: Less than
# <=: Less than or equal to
# >: Greater than
# >=: Greater than or equal to
# in_: In a list of values
# not_in_: Not in a list of values

@router.get("/test_queries_2")
async def test_queries_2(session: async_sessionmaker = Depends(get_session)):
    # query = await session.execute(select(func.count(StudentModel.id))
    #                                         .where(
    #                                             StudentModel.room_id.in_(select(RoomModel.id).where(
    #                                                 RoomModel.block_id.in_(select(BlockModel.id).where(
    #                                                       or_( BlockModel.airy == 'YES',
    #                                                             BlockModel.water_access == 'YES',
    #                                                             BlockModel.proxy_to_portals_lodge == 'YES'
    #                                                         )
    #                                                 ))
    #                                             ))
    #                                         ).where(StudentModel.medical_attention == 'YES')
    #                                         )
    # query_res = query.scalar_one()

    # query2 = await session.execute(select(func.sum(RoomModel.capacity), func.sum(RoomModel.num_space_occupied))
    #                                         .join(BlockModel, RoomModel.block_id == BlockModel.id)
    #                                         .where(BlockModel.id == 77)
    #                                         .where(BlockModel.gender == "F")
    #                                         .with_for_update())
    # used_capacity = query2.fetchone()
    
    query_f = await session.execute(select(func.count(StudentModel.id))
                                            .where( StudentModel.room_id.in_(select(RoomModel.id).where(
                                                    RoomModel.block_id.in_(select(BlockModel.id).where(
                                                          or_( BlockModel.airy == 'YES',BlockModel.water_access == 'YES',
                                                                BlockModel.proxy_to_portals_lodge == 'YES' ) ))
                                                ).where(RoomModel.block_id.in_([55,56]))) ).where(StudentModel.medical_attention == 'YES'))
    query_res = query_f.scalar_one()
    
    q2 = await session.execute(select(BlockProximityToFacultyModel.block_id).where(BlockProximityToFacultyModel.faculty == '14'))
    res = q2.scalars().all()
    print("####################11111111")
    print(res)
    return {"message":"Testing2"}


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


# create block data 

blocks_6000 = [
    {
 "block_name": "block 2", 
  "description": "Joseph", 
  "gender":"F", 
  "num_rooms_in_block": 36, 
  "norm_room_capacity": 3,
  "corn_room_capacity": 6,
  "num_corn_rooms_in_block": 4, 
  "corner_rooms": [{"value": "2"},{"value": "4"},{"value": "6"},{"value": "8"}], 
  "block_access_to_fac" : [{"value": "4"},{"value": "7"}],
  "access_to_lodge": True,
  "airy": True, 
  "water": False
},

   {
 "block_name": "block 2", 
  "description": "Daniel", 
  "gender":"F", 
  "num_rooms_in_block": 36, 
  "norm_room_capacity": 3,
  "corn_room_capacity": 6,
  "num_corn_rooms_in_block": 4, 
  "corner_rooms": [{"value": "2"},{"value": "4"},{"value": "6"},{"value": "8"}], 
  "block_access_to_fac" : [{"value": "3"},{"value": "5"},{"value": "3"},{"value": "5"},],
  "access_to_lodge": True,
  "airy": True, 
  "water": False
},

   {
 "block_name": "block 2", 
  "description": "Adeboya", 
  "gender":"F", 
  "num_rooms_in_block": 36, 
  "norm_room_capacity": 3,
  "corn_room_capacity": 6,
  "num_corn_rooms_in_block": 4, 
  "corner_rooms": [{"value": "2"},{"value": "4"},{"value": "6"},{"value": "8"}], 
  "block_access_to_fac" : [{"value": "8"},{"value": "5"},{"value": "6"},{"value": "2"},],
  "access_to_lodge": True,
  "airy": True, 
  "water": False
},

  {
 "block_name": "block 2", 
  "description": "Enouch", 
  "gender":"F", 
  "num_rooms_in_block": 36, 
  "norm_room_capacity": 3,
  "corn_room_capacity": 6,
  "num_corn_rooms_in_block": 4, 
  "corner_rooms": [{"value": "2"},{"value": "4"},{"value": "6"},{"value": "8"}], 
  "block_access_to_fac" : [{"value": "4"},{"value": "5"},{"value": "6"},{"value": "7"},],
  "access_to_lodge": True,
  "airy": True, 
  "water": False
},

  {
 "block_name": "block 2", 
  "description": "Psalmist", 
  "gender":"F", 
  "num_rooms_in_block": 36, 
  "norm_room_capacity": 3,
  "corn_room_capacity": 6,
  "num_corn_rooms_in_block": 4, 
  "corner_rooms": [{"value": "2"},{"value": "4"},{"value": "6"},{"value": "8"}], 
  "block_access_to_fac" : [{"value": "1"},{"value": "2"},{"value": "3"},{"value": "4"},],
  "access_to_lodge": True,
  "airy": True, 
  "water": False
},
    {
 "block_name": "block 2", 
  "description": "Elijah", 
  "gender":"F", 
  "num_rooms_in_block": 36, 
  "norm_room_capacity": 3,
  "corn_room_capacity": 6,
  "num_corn_rooms_in_block": 4, 
  "corner_rooms": [{"value": "2"},{"value": "4"},{"value": "6"},{"value": "8"}], 
  "block_access_to_fac" : [{"value": "4"},{"value": "7"}],
  "access_to_lodge": True,
  "airy": True, 
  "water": False
},

]


@router.post("/load_dummy")
async def test_queries(session: async_sessionmaker = Depends(get_session)):
    for i in range(28): 
        random_number = random.randint(0, 5)
        block_obj = blocks_6000[random_number]
        block_obj['block_name'] = f"Block {i+1}"
        data = BlockSchemaCreate(**block_obj)
        # res = await admin_service.create_new_block_db_service(data,session)  used 
        
        await asyncio.sleep(1)
    return {"message":"Testing"}




# {
#  "block_name": "block 2", 
#   "description": "Bachelor Degree", 
#   "gender":"M", 
#   "num_rooms_in_block": 36, 
#   "norm_room_capacity": 3,
#   "corn_room_capacity": 6,
#   "num_corn_rooms_in_block": 2, 
#   "corner_rooms": [{"value": "4", "label": "BASIC MEDICAL SCIENCES"},{"value": "7", "label": "BASIC MEDICAL SCIENCES"}], 
#   "block_access_to_fac" : [{"value": "4", "label": "BASIC MEDICAL SCIENCES"},{"value": "7", "label": "BASIC MEDICAL SCIENCES"}],
#   "access_to_lodge": true,
#   "airy": true, 
#   "water": false
# }