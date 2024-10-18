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
#  



async def get_student_profile_and_allocate_room_to_the_student_service(mat_no:str,user_meta,  session):
    stud_profile =  external_services.get_student_profile_in_session_given_matno(mat_no)
    curr_session = '2024/2025' #external_services.get_current_academic_session()
    if stud_profile[0]:
        if curr_session[0]:
            stud_obj = stud_profile[1]
            stud_obj['matric_number'] = mat_no
            stud_obj['curr_session'] = curr_session[1]
            stud_obj['medical_attention']= admin_service_helper1.list_of_matric_number_with_health_issue(mat_no)
            res = await admin_service.first_condition_before_ramdom_room_allocation(stud_obj,user_meta,session)
            if res[0]:
                return True,res[1]
            return False,res[1]
        else:
            return False,curr_session[1]
    else:
        return False,stud_profile[1]





