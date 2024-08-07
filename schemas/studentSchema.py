from pydantic import BaseModel, EmailStr, constr,field_validator
from datetime import datetime   
from schemas.helperSchema import Gender,BlockStatus,Deleted
from schemas.roomSchema import RoomSchemaDetailed
from typing import List



class StudentRoomSchema(BaseModel):
    id: int
    matric_number: str
    room_id: int
    acad_session: str
    deleted: str
    created_at: str
    updated_at: str


class StudentInBlockchema(BaseModel):
    id: int
    matric_number: str
    room_id: int
    acad_session: str
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
