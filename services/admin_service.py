from typing import List
from fastapi import HTTPException
from sqlalchemy.future import select
from models.userModel import UserModel,BlockModel,RoomModel
from schemas.userSchema import CreateUser,ListUser,ReturnSignUpUser,ListUser2
from schemas.blockSchemas import BlockSchema,GetRoomStat
from schemas.roomSchema import RoomSchema
from services import admin_service_helper1
from api.endpoints import endpoint_helper
from services.external_services import verify_supplied_email_from_staff_portal
from sqlalchemy.ext.asyncio import async_sessionmaker



async def sign_up_service(user_create:CreateUser, session:async_sessionmaker) -> ListUser:
   user_create = user_create.model_dump()
   status,data = verify_supplied_email_from_staff_portal(user_create["email"],user_create["password"])
   if status:
       try:
            user_create["password"] = endpoint_helper.get_password_hashed(user_create["password"])
            _user = UserModel(**user_create)
            session.add(_user)
            await session.commit()
            await session.refresh(_user)
            return True,admin_service_helper1.build_response_dict(_user,ReturnSignUpUser)
       except Exception as e:
            await session.rollback()
            return False, {"message":"Error creating user, maybe duplicate entry for email"}
   else:
       return False, data


async def list_user_service(session:async_sessionmaker) -> List[ListUser]:
      result = await session.execute(select(UserModel))
      users = result.scalars().all()
      return users


async def get_user_by_email_service(email:str, session:async_sessionmaker) -> ListUser:
   result = await session.execute(select(UserModel.id, UserModel.email,UserModel.status,UserModel.created_at,
                                        UserModel.updated_at ).where(UserModel.email == email))
   user = result.fetchone()  
   if not user:
       return False
   return admin_service_helper1.build_response_dict(user,ListUser)
     

async def get_user_4_auth_by_email_service(email:str, session:async_sessionmaker):
   try:
       result = await session.execute(select(UserModel.id, UserModel.email,UserModel.password,UserModel.status,UserModel.created_at,
                                        UserModel.updated_at ).where(UserModel.email == email))
       user = result.fetchone()
       if not user:
           return False , {"message":f"No user found with the email {email}"}
       formated_data = admin_service_helper1.build_response_dict(user,ListUser2)
   except:
       return False, {"message":"Error querying db from get_user_4_auth_by_email_service or build_response_dict"}
   else:
    #    if isinstance(formated_data, dict):
        return True, formated_data
      
   finally:
       pass
  


async def create_new_block_db_service(input:BlockSchema, session:async_sessionmaker):
    try:
        block = input.model_dump()
        if not admin_service_helper1.validate_input_num_of_room_in_block(block)[0]:
            return False,{"message":admin_service_helper1.validate_input_num_of_room_in_block(block)[1]} 
        block = BlockModel(**block)
        session.add(block)
        await session.commit()
        await session.refresh(block)
        list_room_num = [num for num in range(1, block.num_rooms_in_block+1)]
        list_of_norm_room_num = [norm for norm in list_room_num if norm not in [12,18,32]]
        norm_room_objs = [RoomModel(rooms_name= f"room_{i}",capacity="3", room_type="NORMAL",block_id = block.id) 
                                for i in list_of_norm_room_num]
        session.add_all(norm_room_objs)
        await session.commit()
        corn_room_objs = [RoomModel(rooms_name= f"room_{i}",capacity="4", room_type="CORNER",block_id = block.id) 
                                for i in [12,18,32]]
        session.add_all(corn_room_objs)
        await session.commit()
    except:
         await session.rollback()
         return False,{"message":"Error creating block and rooms"} 
    else:
         block_dict = admin_service_helper1.build_response_dict(block,BlockSchema) 
         list_norm_rooms_created = [admin_service_helper1.build_response_dict(norm_obj,RoomSchema)  for norm_obj in norm_room_objs ]
         list_corn_rooms_created = [admin_service_helper1.build_response_dict(corn_obj,RoomSchema)  for corn_obj in corn_room_objs ]
         block_dict.update({"norm_room":list_norm_rooms_created, "corner_room":list_corn_rooms_created})
         return True,block_dict
    finally:
        pass
    




async def get_rooms_stat_service(session:async_sessionmaker):
   try:
       result = await session.execute(select(BlockModel.num_norm_rooms_in_block,BlockModel.num_corn_rooms_in_block,
                                      BlockModel.gender ).where(BlockModel.deleted == 'N'))
       room_block_stat = result.all()
       sum_male_norm_rooms = sum([ row[0] for row in room_block_stat if row[2].value == 'M'])
       sum_male_corn_rooms = sum([ row[1] for row in room_block_stat if row[2].value == 'M'])
       sum_female_norm_rooms = sum([ row[0] for row in room_block_stat if row[2].value == 'F'])
       sum_female_corn_rooms = sum([ row[1] for row in room_block_stat if row[2].value == 'F'])
   except:
       return False,{"Message":"Error fetching or summing blocks/rooms statistics"}
   else:
       return True,{'male_norm_room':sum_male_norm_rooms,'male_c_room':sum_male_corn_rooms,
                    'female_norm_room':sum_female_norm_rooms,'female_c_room':sum_female_corn_rooms}


# 
async def get_all_available_rooms_from_selected_block_service(block_id:int, session:async_sessionmaker):
   try:
       result = await session.execute(select(RoomModel.id, RoomModel.rooms_name,RoomModel.capacity,
                                       RoomModel.room_type, RoomModel.block_id,RoomModel.room_status,RoomModel.room_condition   
                                       ).where(RoomModel.block_id == block_id,RoomModel.room_status =='AVAILABLE',RoomModel.deleted == 'N'))
       room_list = result.all()
       resp = [admin_service_helper1.build_response_dict(room,RoomSchema)  for room in room_list]
   except:
       return False, {"message":"Error fetching all available in block rooms given block ID"}
   else:
       return True,resp


# session.query(UserModel).filter_by(email=email).first()
# session.query(UserModel.id).filter_by(email=email).scalar_one_or_none()
# scalar_one_or_none()
# first()


