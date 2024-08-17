from typing import List
from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy import func,distinct
from models.userModel import UserModel,BlockModel,RoomModel,StudentModel,BlockProximityToFacultyModel
from schemas.userSchema import CreateUser,ListUser,ReturnSignUpUser,ListUser2
from schemas.blockSchemas import BlockSchema,GetRoomStat,BlockRoomSchema2
from schemas.roomSchema import RoomSchema,RoomSchemaDetailed,RoomStatusSchema
from schemas.studentSchema import StudentRoomSchema,StudentInBlockchema
from schemas.helperSchema import Gender,RoomCondition
from services import admin_service_helper1
from services import admin_service_helper2
from api.endpoints import endpoint_helper
from services import external_services 
from sqlalchemy.ext.asyncio import async_sessionmaker
from services import admin_service



async def get_student_profile_and_allocate_room_to_the_student(mat_no:str, session_id:str, session):
    stud_profile =  external_services.get_student_profile_in_session_given_matno(mat_no)
    if stud_profile[0]:
        stud_obj = stud_profile[1]
        stud_obj['matric_number'] = mat_no
        stud_obj['curr_session'] = session_id
        if int(stud_obj['accom_paid']) < int(stud_obj['accom_payable']) :
            return False, {"message": f"#{stud_obj['accom_payable']}  is the amount payable for accommodation but you have just paid #{int(stud_obj['accom_paid'])}"}
        elif int(stud_obj['accom_paid']) >= int(stud_obj['accom_payable']) :
            get_room_condition = {'room_cat':''}
            if (int(stud_obj['special_accom_paid']) >= int(stud_obj['special_accom_paid'])) and int(stud_obj['special_accom_paid']) > 0:
                get_room_condition['room_cat'] = 'SPECIAL'
                # fake response
                return True, {"room_cat":"SPECIAL","id":"23", "room_name":"room 13", "capacity":2,"room_type":"normal room","block_id":12,"block_name":"Guess House","block desc":"Guess House ", "room_condition":"GOOD" }              
                res = await admin_service.random_assign_room_to_student_in_session_service(stud_obj,get_room_condition,session)
                return res
            elif int(stud_obj['special_accom_paid']) == -1 and (int(stud_obj['accom_paid']) >= int(stud_obj['accom_payable']) ):
                get_room_condition['room_cat'] = 'GENERAL'
                # fake response
                return True, {"room_cat":"GENERAL","id":"23", "room_name":"room 13", "capacity":6,"room_type":"cornal room","block_id":12,"block_name":"block 2","block desc":"Joseph", "room_condition":"GOOD" }             
                res = await admin_service.random_assign_room_to_student_in_session_service(stud_obj,get_room_condition,session)
                return res
            else:
                return False,{"message":"Ops!! I doubt if you have actually paid minimum requirement for accommodation in this session"}
        else:
            return False,{"message":"Sorry!! Your acclaimed payment for accommodation can not be verified now"}
    else:
        return False,stud_profile[1]


