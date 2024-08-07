from typing import List
from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy import func,distinct
from models.userModel import UserModel,BlockModel,RoomModel,StudentModel
from schemas.userSchema import CreateUser,ListUser,ReturnSignUpUser,ListUser2
from schemas.blockSchemas import BlockSchema,GetRoomStat,BlockRoomSchema2
from schemas.roomSchema import RoomSchema,RoomSchemaDetailed,RoomStatusSchema
from schemas.studentSchema import StudentRoomSchema,StudentInBlockchema
from schemas.helperSchema import Gender,RoomCondition
from services import admin_service_helper1
from services import admin_service_helper2
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
       result = await session.execute(select(UserModel.id, UserModel.email,UserModel.password,UserModel.status,
                                             UserModel.gender,UserModel.user_type,UserModel.created_at,
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
                                       ).where(RoomModel.block_id == block_id,RoomModel.room_status =='AVAILABLE',RoomModel.room_condition =='GOOD',RoomModel.deleted == 'N'))
       room_list = result.all()
       resp = [admin_service_helper1.build_response_dict(room,RoomSchema)  for room in room_list]
   except:
       return False, {"message":"Error fetching all available in block rooms given block ID"}
   else:
       return True,resp



async def get_all_occupied_rooms_from_selected_block_service(block_id:int, session:async_sessionmaker):
   try:
        result = await session.execute(select(RoomModel.id, RoomModel.rooms_name,RoomModel.capacity,
                                        RoomModel.room_type, RoomModel.block_id,RoomModel.room_status,RoomModel.room_condition,  
                                        BlockModel.block_name)
                                        .join(BlockModel, RoomModel.block_id == BlockModel.id)
                                        .where(RoomModel.block_id == block_id,RoomModel.room_status =='OCCUPIED',RoomModel.deleted == 'N'))
        room_list = result.all()
        resp = [admin_service_helper1.build_response_dict(room,RoomSchema)  for room in room_list]
   except:
        return False, {"message":"Error fetching all available in block rooms given block ID"}
   else:
        return True,resp



async def random_assign_room_to_student_in_session_service(mat_no:str,gender:Gender, session:async_sessionmaker):
    curr_session = '2023/2024'
    check_for_stud_room = await admin_service_helper2.get_student_room_in_session(mat_no,curr_session,session)
    if not check_for_stud_room[0]:
        get_room = await admin_service_helper2.get_random_available_room(gender, curr_session,session)
        if get_room[0]:
            allo_room = await admin_service_helper2.room_allocation_service(mat_no,get_room[1]['id'],get_room[1]['block_id'],
                                                                            get_room[1]['num_rooms_in_block'], get_room[1]['num_of_allocated_rooms'],
                                                                            curr_session,get_room[1]['capacity'],session)
            if allo_room:
                return True,allo_room[1]
        else:
            return False, get_room[1] 
    else:
        return True, check_for_stud_room[1]
    


async def assign_room_in_specific_block_to_student_in_session_service(mat_no:str,gender:Gender,block_id:int, session:async_sessionmaker):
    curr_session = '2023/2024'
    check_for_stud_room = await admin_service_helper2.get_student_room_in_session(mat_no,curr_session,session)
    if not check_for_stud_room[0]:
        get_room = await admin_service_helper2.get_specific_available_room_in_block(gender, curr_session,block_id,session)
        if get_room[0]:
            allo_room = await admin_service_helper2.room_allocation_service(mat_no,get_room[1]['id'],get_room[1]['block_id'],
                                                                            get_room[1]['num_rooms_in_block'], get_room[1]['num_of_allocated_rooms'],
                                                                            curr_session,get_room[1]['capacity'],session)
            if allo_room:
                return True,allo_room[1]
        else:
            return False, get_room[1] 
    else:
        return True, check_for_stud_room[1]




async def assign_specific_space_in_room_to_student_in_session_service(mat_no:str,gender:Gender,room_id:int, session:async_sessionmaker):
    curr_session = '2023/2024'
    check_for_stud_room = await admin_service_helper2.get_student_room_in_session(mat_no,curr_session,session)
    if not check_for_stud_room[0]:
        get_room = await admin_service_helper2.get_specific_available_space_in_room(gender, curr_session,room_id,session)
        if get_room[0]:
            allo_room = await admin_service_helper2.room_allocation_service(mat_no,get_room[1]['id'],get_room[1]['block_id'],
                                                                            get_room[1]['num_rooms_in_block'], get_room[1]['num_of_allocated_rooms'],
                                                                            curr_session,get_room[1]['capacity'],session)
            if allo_room:
                return True,allo_room[1]
        else:
            return False, get_room[1] 
    else:
        return True, check_for_stud_room[1]



async def get_student_room_in_session_service(mat_no:str,session_id:str, session:async_sessionmaker):
    stud_room = await admin_service_helper2.get_student_room_in_session(mat_no,session_id,session)
    if not stud_room[0]:
        return False, stud_room[1]
    else:
        return True,stud_room[1]


async def delete_student_from_room_in_session_service(mat_no:str,session_id:str, session:async_sessionmaker):
     stud_room = await admin_service_helper2.get_student_room_in_session(mat_no,session_id,session)
     if stud_room[0]:
         await admin_service_helper2.decre_update_block_record_given_block_id(stud_room[1]['room_details']['block_id'],session)
         res = await admin_service_helper2.decre_update_room_status_given_room_id(stud_room[1]['room_id'],stud_room[1]['id'],session)
         await session.commit()
         return True,res[1]
     else:
         return False, stud_room[1]



async def list_student_in_room_in_session_service(room_id:int, session:async_sessionmaker):
    try:
        stud_in_room = await session.execute(select(StudentModel.id,StudentModel.matric_number,StudentModel.room_id,
                                            StudentModel.acad_session,StudentModel.deleted,StudentModel.created_at,StudentModel.updated_at)
                                    .where(StudentModel.room_id == room_id))
        result =  stud_in_room.all()
        if result:
            resp = [admin_service_helper1.build_response_dict(room,StudentRoomSchema)  for room in result]
            return True,resp
        else:
            return False, {"message":"No student allocated to this room yet"}
    except:
        return False, {"message":f"Error fetching students in the room with id {room_id}"}


async def get_room_status_in_session_service(room_id:int, session:async_sessionmaker):
    try:
        query = await session.execute(select(RoomModel.id,RoomModel.rooms_name,RoomModel.capacity,RoomModel.room_type,
                                            RoomModel.block_id,RoomModel.room_status,RoomModel.room_condition,
                                            RoomModel.deleted,RoomModel.created_at,RoomModel.updated_at
                                            ).where(RoomModel.id == room_id))
        room_status = query.fetchone()
        if room_status:
            return True, admin_service_helper1.build_response_dict(room_status,RoomStatusSchema) 
        else:
            return False, {"message":f"No room found with id {room_id}"}
    except:
        return False, {"message":f"Error querying room with id {room_id}"}
    

async def  update_room_condition_in_session_service(room_id:int,room_condition:RoomCondition, session:async_sessionmaker):
   try:
        query = await session.execute(select(RoomModel).where(RoomModel.id == room_id))
        query_res = query.scalar_one()
        if query_res:
            query_res.room_condition = room_condition
            await session.commit()
            return True, {"message":"Room condition successfully updated"}
        else:
            return False, {"message":f"No room with id {room_id} is available for update"}

   except:
       return False, {"message":f"Error updating room condition with id {room_id}"}



async def list_rooms_with_empty_space_in_session_service(gender:Gender, session_id, session:async_sessionmaker):
    try:
        # query = await session.execute(select(distinct(StudentModel.room_id)).where(StudentModel.acad_session==session_id))
        # list_occupied_room_in_session_id = query.scalars().all()
        get_room = await session.execute(select(RoomModel.id, RoomModel.rooms_name,RoomModel.capacity,BlockModel.block_name,BlockModel.num_rooms_in_block,
                                            BlockModel.num_of_allocated_rooms, BlockModel.gender,RoomModel.room_type, RoomModel.block_id,RoomModel.room_status,RoomModel.room_condition )
                                            .join(BlockModel, RoomModel.block_id == BlockModel.id)
                                            .where(RoomModel.room_status == "AVAILABLE")
                                            .where(BlockModel.block_status == "AVAILABLE")
                                            .where(BlockModel.gender == gender))
        rooms =  get_room.all()
        if not rooms:
            return False, {"message":"No empty space/room found"}
        format_data = [admin_service_helper1.build_response_dict(room,RoomSchemaDetailed) for room in rooms ]
        return True, format_data

    except:
        return False, {"message":"Database error fetching list_rooms_with_empty_space_in_session_service"}


async def list_occupied_rooms_in_session_service(gender:Gender, session_id, session:async_sessionmaker):
    try:
        get_room = await session.execute(select(RoomModel.id, RoomModel.rooms_name,RoomModel.capacity,BlockModel.block_name,BlockModel.num_rooms_in_block,
                                            BlockModel.num_of_allocated_rooms, BlockModel.gender,RoomModel.room_type, RoomModel.block_id,RoomModel.room_status,RoomModel.room_condition )
                                            .join(BlockModel, RoomModel.block_id == BlockModel.id)
                                            .where(RoomModel.room_status == "OCCUPIED")
                                            .where(BlockModel.gender == gender))
        rooms =  get_room.all()
        if not rooms:
            return False, {"message":"No occupied room found..."}
        format_data = [admin_service_helper1.build_response_dict(room,RoomSchemaDetailed) for room in rooms ]
        return True, format_data

    except:
        return False, {"message":"Database error fetching list_rooms_with_empty_space_in_session_service"}


async def list_blocks_with_empty_rooms_in_session_service(gender:Gender, session:async_sessionmaker):
    try:
        get_block = await session.execute(select(BlockModel.id,BlockModel.block_name,BlockModel.description,BlockModel.gender,BlockModel.block_status,
                                                BlockModel.num_rooms_in_block,BlockModel.num_of_allocated_rooms,
                                                BlockModel.num_norm_rooms_in_block, BlockModel.num_corn_rooms_in_block,
                                                BlockModel.created_at,BlockModel.updated_at, BlockModel.deleted)
                                            .where(BlockModel.block_status == "AVAILABLE")
                                            .where(BlockModel.gender == gender))
        blocks =  get_block.all()
        if not blocks:
            return False, {"message":"No available block found..."}
        format_data = [admin_service_helper1.build_response_dict(block,BlockRoomSchema2) for block in blocks ]
        return True, format_data
    except:
        return False, {"message":"Database error fetching list_blocks_with_empty_rooms_in_session_service"}
 

async def list_students_with_accomodation_in_block_in_session_service(block_id:int,  session:async_sessionmaker):
    try:
        query = await session.execute(select(StudentModel.id, StudentModel.matric_number,StudentModel.acad_session,
                                            StudentModel.room_id,StudentModel.created_at, StudentModel.updated_at,
                                            RoomModel.rooms_name, RoomModel.capacity,RoomModel.room_type,RoomModel.room_status,RoomModel.room_condition,
                                            BlockModel.block_name,BlockModel.gender,BlockModel.description)
                                            .join(RoomModel, StudentModel.room_id == RoomModel.id)
                                            .join(BlockModel, RoomModel.block_id == BlockModel.id )
                                            .where(BlockModel.id  == block_id))
        studs = query.all()
        if not studs:
                return False, {"message":"No student found in the block ..."}
        format_data = [admin_service_helper1.build_response_dict(stud,StudentInBlockchema) for stud in studs ]
        return True, format_data    
    except:
        return False, {"message":"Database error fetching list_students_with_accomodation_in_block_in_session_service"}        
# 
# NOTE:  fetchone() vs scalar_one()
# .where(RoomModel.id.notin_(list_occupied_room_in_session_id))