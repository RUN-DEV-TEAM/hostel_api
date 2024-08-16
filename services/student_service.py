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
        stud_profile_matno = stud_profile[1]
        stud_profile_matno['matric_number'] = mat_no
        if int(stud_profile_matno['accom_payable']) != int(stud_profile_matno['accom_paid']):
            diff = int(stud_profile_matno['accom_payable']) - int(stud_profile_matno['accom_paid'])
            return False, {"message": f"#{stud_profile_matno['accom_payable']}  is the amount payable for accommodation but you have just paid #{diff}"}
        else:
            res = await admin_service.random_assign_room_to_student_in_session_service(stud_profile_matno,session)
            return res
    else:
        return False,stud_profile[1]


