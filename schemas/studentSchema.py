from pydantic import BaseModel, EmailStr, constr,field_validator
from datetime import datetime   
from schemas.helperSchema import Gender,BlockStatus,Deleted
from schemas.roomSchema import RoomSchemaDetailed
from typing import List

class StudentProfileSchema(BaseModel):
    matric_number: str
    surname: str
    firstname: str
    othername:str
    prog_id: str
    level: str



class StudentRoomSchema(BaseModel):
    id: int
    matric_number: str
    room_id: int
    curr_session: str
    deleted: str
    created_at: str
    updated_at: str





class ListStudentInRoomSchema(BaseModel):
    id: int
    matric_number: str
    surname: str
    firstname: str
    sex: str
    level: str
    program: str
    dpt: str
    college: str
    room_id: int
    curr_session: str
    created_at: str
    updated_at: str



class StudentInBlockchema(BaseModel):
    id: int
    matric_number: str
    surname: str
    firstname: str
    level: str
    program: str
    dpt: str
    college: str
    room_id: int
    curr_session: str
    created_at: str
    updated_at: str
    rooms_name: str
    capacity: int
    room_type: str
    room_status: str
    room_condition: str
    block_name: str
    gender: str
    description: str

                                 
class ListAllOccupantSchemaResponse(BaseModel):
    matric_number: str
    surname: str
    firstname: str
    gender: str
    level: str
    program: str
    college: str
    room_id :str
    room_name :str
    capacity: str
    RoomModel: str
    room_type: str
    block_name: str
    description: str
    curr_session: str
    created_at : str
    updated_at: str

