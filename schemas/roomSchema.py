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
    room_status : str
    room_condition : str


