from pydantic import BaseModel, EmailStr, constr,field_validator
from datetime import datetime   
from schemas.helperSchema import Gender,BlockStatus,Deleted
from typing import List


class RoomSchema(BaseModel):
    id : int
    rooms_name : str
    capacity : str 
    room_type: str
    block_id : int 
    block_name : str
    room_status : str
    room_condition : str


class RoomStatusSchema(BaseModel):
    id : int
    rooms_name : str
    capacity : str 
    room_type: str
    block_id : int 
    room_status : str
    room_condition : str
    deleted: str
    created_at: str
    updated_at: str



class RoomSchemaDetailed(BaseModel):
    id : int
    rooms_name : str
    capacity : str 
    room_type: str
    block_id : int 
    block_name : str
    num_rooms_in_block:int
    num_of_allocated_rooms:int
    gender: str
    room_status : str
    room_condition : str



# class RoomAllocationParamSchema(BaseModel):
#     matric_number:str
#     room_id:int
#     acad_session:str


class RoomAllocationResponseSchema(BaseModel):
    matric_number:str
    room_id:int
    acad_session:str