from pydantic import BaseModel, EmailStr, constr,field_validator
from datetime import datetime   
from schemas.helperSchema import Gender,BlockStatus,Deleted
from typing import List


class BlockProxityResponse(BaseModel):
    faculty : int


class BlockRoomSchema(BaseModel):
    block_name : str
    description : str
    gender : Gender 
    num_rooms_in_block: int
    num_of_allocated_rooms : int = 0
    num_norm_rooms_in_block : int = 0
    norm_room : List[dict] = {}
    num_corn_rooms_in_block : int = 0
    corner_room : List[dict] = {}
    block_status : BlockStatus
    deleted : Deleted


class BlockRoomSchema2(BaseModel):
    id: int
    block_name : str
    description : str
    gender : Gender 
    num_rooms_in_block: int
    num_of_allocated_rooms : int = 0
    num_norm_rooms_in_block : int = 0
    num_corn_rooms_in_block : int = 0
    block_status : BlockStatus
    deleted : Deleted
    created_at: str
    updated_at: str



class BlockSchemaCreate(BaseModel):
    block_name : str
    description : str
    gender : str 
    num_rooms_in_block: int
    num_corn_rooms_in_block : int = 0
    norm_room_capacity: int
    corn_room_capacity: int
    corner_rooms: List[dict] |str = []
    block_access_to_fac: List[dict]  = []
    access_to_lodge: bool = False
    airy: bool = False
    water: bool = False



class BlockSchemaCreateResponse(BaseModel):
    block_name : str
    description : str
    gender : str 
    num_rooms_in_block: int
    num_of_allocated_rooms : int = 0
    num_norm_rooms_in_block : int = 0
    num_corn_rooms_in_block : int = 0
    block_status: str
    deleted: str
    norm_room: List[dict] = []
    corner_room: List[dict] = []
    block_access_to_fac: List[dict]  = []
    access_to_lodge: bool = False
    airy: bool = False
    water: bool = False


class BlockSchema(BaseModel):
    block_name : str
    description : str
    gender : Gender 
    num_rooms_in_block: int
    num_of_allocated_rooms : int = 0
    num_norm_rooms_in_block : int = 0
    num_corn_rooms_in_block : int = 0
    block_status : BlockStatus
    deleted : Deleted

    @field_validator("block_status")
    def set_default_block_status(cls, value):
        if value is None:
            return BlockStatus.AVAILABLE  # Set the default to green
        return value
    
    @field_validator("deleted")
    def set_default_deleted(cls, value):
        if value is None:
            return Deleted.N  # Set the default to green
        return value

    # @field_validator("num_rooms_in_block")
    # def set_default_num_rooms_in_block(cls, value):
    #     if value <= 0:
    #         raise CustomValidationError("num_rooms_in_block", "Number of rooms in block can not be zero or negative!!")
    #     return value
    





class CustomValidationError(Exception):
    def __init__(self, name: str, message: str):
        self.name = name
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.name}: {self.message}"
    


class GetRoomStat(BaseModel):
    female_norm_room: int = 0
    female_c_room : int = 0
    male_norm_room : int = 0
    male_c_room : int = 0



class ListAllBlockSchemeResponse(BaseModel):
    id: int
    block_name: str
    description: str
    gender: str
    num_rooms_in_block: int
    num_norm_rooms_in_block: int
    num_corn_rooms_in_block: int
    num_of_allocated_rooms: int
    block_status: str
    airy: bool
    water_access: bool
    proxy_to_portals_lodge: bool
    created_at : str
   
