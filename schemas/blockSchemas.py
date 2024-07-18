from pydantic import BaseModel, EmailStr, constr,field_validator
from datetime import datetime   
from schemas.helperSchema import Gender,BlockStatus,Deleted


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