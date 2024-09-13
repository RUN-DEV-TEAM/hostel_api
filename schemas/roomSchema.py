from pydantic import BaseModel, EmailStr, constr,field_validator
from datetime import datetime   
from schemas.helperSchema import Gender,BlockStatus,Deleted
from typing import List




class UpdateRoomSchema(BaseModel):
    id : int
    room_name : str
    capacity : str 
    room_type: str
    room_status : str
    room_condition : str

class RoomSchemaWithOutBlockName(BaseModel):
    id : int
    room_name : str
    capacity : str 
    num_space_occupied : str
    room_type: str
    block_id : int 
    room_status : str
    room_condition : str

class RoomSchema(BaseModel):
    id : int
    room_name : str
    capacity : str 
    room_type: str
    block_id : int 
    block_name : str
    room_status : str
    room_condition : str


class RoomStatusSchema(BaseModel):
    id : int
    room_name : str
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
    room_name : str
    capacity : str 
    room_type: str
    block_id : int 
    block_name : str
    description: str
    num_rooms_in_block: int
    num_of_allocated_rooms: int
    room_status : str
    room_condition : str


# class RoomSchemaDetailedResponse(BaseModel):
#     id : int
#     room_name : str
#     capacity : str 
#     room_type: str
#     block_id : int 
#     block_name : str
#     room_status : str
#     room_condition : str



# class RoomAllocationParamSchema(BaseModel):
#     matric_number:str
#     room_id:int
#     acad_session:str


class RoomAllocationResponseSchema(BaseModel):
    id: int
    matric_number:str
    surname:str
    firstname:str
    sex:str
    medical_attention: str
    program: str
    level: str
    curr_session:str
    created_at: str
    

class RoomSchemaDetailedResponse(BaseModel):
    id : int
    room_name : str
    capacity : int 
    num_space_occupied: int
    room_type: str
    block_id : int 
    block_name : str
    description: str
