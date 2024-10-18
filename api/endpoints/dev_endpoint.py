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
    
    # query_f = await session.execute(select(func.count(StudentModel.id))
    #                                         .where( StudentModel.room_id.in_(select(RoomModel.id)
    #                                                 .where(RoomModel.block_id.in_(
    #                                                  select(BlockModel.id).where(BlockModel.proxy_to_portals_lodge == 'YES')
    #                                                 .where(BlockModel.water_access == 'YES')
    #                                                 .where(BlockModel.airy == 'YES')
    #                                                 .where(BlockModel.gender == 'M')
    #                                             ))) ).where(StudentModel.medical_attention == 'YES'))
    # query_res = query_f.scalar_one()
    
    # q2 = await session.execute(select(BlockProximityToFacultyModel.block_id).where(BlockProximityToFacultyModel.faculty == '14'))
    # res = q2.scalars().all()
    # print(query_res)
    query_special_blocks = await session.execute(select(BlockProximityToFacultyModel.block_id)
                                                        .where(BlockProximityToFacultyModel.faculty == '14')
                                                        .where(BlockProximityToFacultyModel.block_id.in_(select(BlockModel.id).where(BlockModel.gender == 'M'))))

    res_query_special_blocks = query_special_blocks.scalars().all() 
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$") 
    print(res_query_special_blocks)
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



@router.post("/delete_dummy")
async def delete_dummy_func(session: async_sessionmaker = Depends(get_session)):
    get_occupant_matr_query = await session.execute(select(StudentModel.matric_number))
    res = get_occupant_matr_query.all()
    for mat in res:
      #  act_res = await admin_service.delete_student_from_room_in_session_service(mat[0], session)
      #  print(act_res)
       await asyncio.sleep(1)
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




import csv
import io

# Your CSV data as a string
csv_data = """
RUN/MCM/22/13442,2,23
RUN/PHY/23/15525,21,3
RUN/THA/22/12467,9,9
Run/bkf/22/12701,9,13
Run/Bus/22/12719,9,12
RUN/QSY/23/14474,31,17
RUN/PSY/22/13669,11,22
RUN/PHT/21/10156,9,24
Run/eco/22/13339,21,4
RUN/BDG/22/11987,11,7
RUN/TTH/23/15875,25,22
RUN/IFT/22/13166,5,2
RUN/PAD/22/12776,2,21
RUN/FRE/23/14679,22,8
RUN/ECO/22/13348,22,3
RUN/NSC/21/10096,18,4
RUN/PUH/22/11910,10,1
RUN/NSC/21/10118,18,6
RUN/HIS/22/12304,15,21
RUN/ESM/21/10458,30,22
RUN/LAW/22/12502,30,40
RUN/LAW/23/14905,11,17
Run/pol/22/13644,9,16
RUN/ACS/22/12699,9,12
RUN/ICH/22/13147,39,5
RUN/PAD/23/15788,25,3
RUN/ECO/22/13345,21,4
RUN/PSY/22/13677,11,22
Run/urp/23/14481,4,9
Run/puh/23/14412,20,24
RUN/ENG/22/12243,25,6
Run/eee/21/10387,30,2
RUN/PHS/22/11850,18,5
RUN/EMT/22/11993,21,1
Run/ich/23/15148,2,14
RUN/ANA/22/11617,7,3
RUN/PHT/22/11889,29,40
RUN/ARC/22/11929,29,12
Run/mcb/22/13229,4,9
RUN/PHT/21/10207,24,16
Run/mee/22/12174,7,3
Run/law/22/12492,9,5
Run/mls/22/11681,29,37
RUN/HIS/22/12278,6,20
RUN/PHS/22/11830,25,4
RUN/ACC/22/12616,8,3
RUN/MCM/22/13484,21,4
RUN/HIS/22/12359,21,5
RUN/MCM/22/13395,6,24
RUN/CMP/22/12882,6,13
RUN/CMP/22/12787,6,13
RUN/IFT/22/13171,6,9
RUN/CMP/22/13007,6,9
RUN/HIS/22/12335,11,22
RUN/ACC/22/12631,6,18
RUN/ACC/22/122661,6,18
RUN/TTH/22/13716,41,19
RUN/CMP/22/12848,6,9
RUN/IFT/22/13192,6,18
RUN/IFT/22/13189,6,18
RUN/CMP/22/12994,6,7
"""

# Convert the string data into a file-like object
csv_file = io.StringIO(csv_data.strip())

# Read the CSV data
csv_reader = csv.reader(csv_file)

# Define headers for the data (assuming it has no headers)
headers = ['mat_no', 'block_no', 'room_no']

# Convert the data into a list of dictionaries
list_of_dicts = [dict(zip(headers, row)) for row in csv_reader]

# Print the result


@router.post("/allocation_for_runsa")
async def test_queries(session: async_sessionmaker = Depends(get_session)):
    for item in list_of_dicts:
      print(str(item['mat_no']).strip().upper())
      print(str(item['block_no']).strip().upper())
      print(str(item['room_no']).strip().upper())


    
    