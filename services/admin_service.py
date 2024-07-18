from typing import List
from fastapi import HTTPException
from sqlalchemy.future import select
from models.userModel import UserModel,BlockModel
from schemas.userSchema import CreateUser,ListUser,ReturnSignUpUser,ListUser2
from schemas.blockSchemas import BlockSchema
from services import admin_service_helper1
from api.endpoints import endpoint_helper
from sqlalchemy.ext.asyncio import async_sessionmaker



async def sign_up_service(user_create:CreateUser, session:async_sessionmaker) -> ListUser:
   user_create = user_create.model_dump()
   user_create["password"] = endpoint_helper.get_password_hashed(user_create["password"])
   _user = UserModel(**user_create)
   try:
        session.add(_user)
        await session.commit()
        await session.refresh(_user)
   except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
   return admin_service_helper1.build_response_dict(_user,ReturnSignUpUser)



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
         return False
       formated_data = admin_service_helper1.build_response_dict(user,ListUser2)
   except:
       return {"status":"failed", "message":"Error querying db from get_user_4_auth_by_email_service or build_response_dict","error":""}
   else:
       if isinstance(formated_data, dict):
            return formated_data
       return False
   finally:
       pass
  

async def create_new_block_db_service(input:BlockSchema, session:async_sessionmaker):
    block = input.model_dump()
    if not admin_service_helper1.validate_input_num_of_room_in_block(block)[0]:
        return {"status":"failed", "message":admin_service_helper1.validate_input_num_of_room_in_block(block)[1],"error":""} 
    block = BlockModel(**block)
    session.add(block)
    await session.commit()
    await session.refresh(block)
    return admin_service_helper1.build_response_dict(block,BlockSchema) 

# session.query(UserModel).filter_by(email=email).first()
# session.query(UserModel.id).filter_by(email=email).scalar_one_or_none()
# scalar_one_or_none()
# first()


# sqlalchemy.exc.InvalidRequestError: When initializing mapper Mapper[Student(t_occupants)], 
# expression 'Room' failed to locate a name ('Room'). If this is a class name, consider adding 
# this relationship() 
# to the <class 'models.studentModel.Student'> class after both dependent classes have been defined.


# {'block_name': 'string', 'description': 'string', 'gender': <Gender.F: 'F'>, 
#  'num_rooms_in_block': 0, 'num_of_allocated_rooms': 0, 'num_norm_rooms_in_block': 0,
#    'num_corn_rooms_in_block': 0, 
#  'block_status': <BlockStatus.OCCUPIED: 'OCCUPIED'>, 'deleted': <Deleted.N: 'N'>}