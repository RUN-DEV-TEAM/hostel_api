from datetime import datetime
from sqlalchemy import func,update, and_,delete, or_
from models.userModel import RoomModel,StudentModel,BlockModel,BlockProximityToFacultyModel
from schemas.roomSchema import RoomSchemaDetailed,RoomAllocationResponseSchema,RoomSchemaDetailedResponse
from schemas.helperSchema import Gender
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.future import select
from services import admin_service_helper1




async def get_student_room_in_session(in_data:dict, session:async_sessionmaker):
   result = await session.execute(select(StudentModel.id,StudentModel.matric_number,StudentModel.room_id,StudentModel.curr_session,
                                         StudentModel.surname,StudentModel.firstname,StudentModel.sex,StudentModel.program,StudentModel.level,
                                         StudentModel.deleted,StudentModel.created_at,StudentModel.updated_at
                                         ).where(StudentModel.matric_number == str(in_data['matric_number']).strip(),
                                                             StudentModel.curr_session == str(in_data['curr_session']).strip()))
   stud_room = result.fetchone()  
   if not stud_room:
       return False, {"message":f"No room for matric number {in_data['matric_number']} in the session {in_data['curr_session']} yet"}
   stud_room_dict = admin_service_helper1.build_response_dict(stud_room,RoomAllocationResponseSchema)
   room_details = await get_room_details_given_student_room_id(stud_room.room_id,session)
   if room_details[0]:
       stud_room_dict.update({"room_details":room_details[1]})
   return True, stud_room_dict



async def backup_room_getter(stud_obj,health_block_counter, session):
    room_res = await query_db_for_random_available_room_with_faculty_proximity_condition(stud_obj, session)
    if room_res[0]:
        return True, admin_service_helper1.build_response_dict(room_res[1],RoomSchemaDetailed)
    else:
        room_res = await default_query_db_for_random_available_room(stud_obj,session)
        if room_res[0]:
            return True, admin_service_helper1.build_response_dict(room_res[1],RoomSchemaDetailed)
        else:
            if health_block_counter > 60:
                room_res = await query_db_for_random_available_room_for_health_challenge_students(stud_obj, session)
                if room_res[0]:
                    return True, admin_service_helper1.build_response_dict(room_res[1],RoomSchemaDetailed)
                else:
                    return False,room_res[1]
            else:
                return False, {"message":"No room available at the moment for allocation"}



async def get_random_available_room(stud_obj:dict,get_room_condition:dict, session:async_sessionmaker):
    
    health_block_counter = 61 #this will be from DB
    if stud_obj['medical_attention'] == 'YES' and health_block_counter <= 60 and get_room_condition['room_cat'] == "GENERAL":
        room_res = await query_db_for_random_available_room_for_health_challenge_students(stud_obj, session)
        if room_res[0]:
            return True, admin_service_helper1.build_response_dict(room_res[1],RoomSchemaDetailed)
        else:
          return await backup_room_getter(stud_obj,health_block_counter, session)
    elif get_room_condition['room_cat'] == "GENERAL":
          return await backup_room_getter(stud_obj,health_block_counter, session)
    elif get_room_condition['room_cat'] == "SPECIAL":
        room_res = await query_db_for_random_room_in_quest_house(stud_obj, session)
        if  room_res[0]:
            return True, admin_service_helper1.build_response_dict(room_res[1],RoomSchemaDetailed)
        else:
            return await backup_room_getter(stud_obj,health_block_counter, session)
    else:
        return False, {"message":"No condition met for getting random available room"}         




async def get_specific_available_room_in_block(gender:Gender,curr_session:str, block_id:int,session:async_sessionmaker):
    get_room = await session.execute(select(RoomModel.id, RoomModel.room_name,RoomModel.capacity ,RoomModel.num_space_occupied,BlockModel.block_name,BlockModel.num_rooms_in_block,
                                           BlockModel.num_of_allocated_rooms, BlockModel.gender,RoomModel.room_type, RoomModel.block_id,RoomModel.room_status,RoomModel.room_condition )
                                        .join(BlockModel, RoomModel.block_id == BlockModel.id)
                                        .where(RoomModel.room_status == "AVAILABLE")
                                        .where(BlockModel.block_status == "AVAILABLE")
                                        .where(BlockModel.gender == gender)
                                        .where(BlockModel.id == block_id)
                                        .with_for_update()
                                        .order_by(func.random())
                                        .limit(1))
    
    room = get_room.fetchone()
    if not room:
       return False, {"message":f"Is like no available room/block for gender {admin_service_helper1.get_full_gender_given_shortName(gender)} in {curr_session} academic session"}
    return True, admin_service_helper1.build_response_dict(room,RoomSchemaDetailed)



async def get_specific_available_space_in_room(in_data:dict, room_id:int,session:async_sessionmaker):
    get_room = await session.execute(select(RoomModel.id, RoomModel.room_name,RoomModel.capacity ,RoomModel.num_space_occupied,BlockModel.block_name,BlockModel.num_rooms_in_block,
                                           BlockModel.num_of_allocated_rooms, BlockModel.gender,RoomModel.room_type, RoomModel.block_id,RoomModel.room_status,RoomModel.room_condition )
                                        .join(BlockModel, RoomModel.block_id == BlockModel.id)
                                        .where(RoomModel.room_status == "AVAILABLE")
                                        .where(BlockModel.block_status == "AVAILABLE")
                                        .where(BlockModel.gender == in_data['sex'])
                                        .where(RoomModel.id == room_id)
                                        .with_for_update()
                                        .order_by(func.random())
                                        .limit(1))
    
    room = get_room.fetchone()
    if not room:
       return False, {"message":f"Is like no available room/block for gender {in_data['sex']}"}
    return True, admin_service_helper1.build_response_dict(room,RoomSchemaDetailed)

 
    
async def room_allocation_service(stud_obj:dict,room_obj:dict,session:async_sessionmaker):
    try:
        _allo_room = StudentModel(room_id=room_obj['id'],**stud_obj)
        session.add(_allo_room)
        await incre_update_room_status_given_room_id(room_obj, session)
        await session.commit()
        await session.refresh(_allo_room)
        room_dict = admin_service_helper1.build_response_dict(_allo_room,RoomAllocationResponseSchema)
        room_details = await get_room_details_given_student_room_id(room_obj['id'],session)
        if room_details[0]:
            room_dict.update({"room_details":room_details[1]})
        return True,room_dict

    except:
        return False, {"message":"Error allocating room"}




async def get_room_details_given_student_room_id(room_id:int, session:async_sessionmaker):
        room_details = await session.execute(select(RoomModel.id, RoomModel.room_name,RoomModel.capacity,RoomModel.num_space_occupied,BlockModel.block_name,BlockModel.description,
                                                    BlockModel.num_rooms_in_block,BlockModel.num_of_allocated_rooms,BlockModel.gender,
                                                RoomModel.room_type, RoomModel.block_id,RoomModel.room_status,RoomModel.room_condition   
                                       )
                                        .join(BlockModel, RoomModel.block_id == BlockModel.id)
                                        .where(RoomModel.id == room_id)
                                        .limit(1))
    
        room_details = room_details.fetchone()
        if not room_details:
            return False, {"message":f"Like no room is foind with the supplied id ::: {room_id}"}
        return True, admin_service_helper1.build_response_dict(room_details,RoomSchemaDetailedResponse)
   


async def get_number_of_occupant_in_room(room_id:int, session:async_sessionmaker):
    try:
        stud_in_room = await session.execute(select(func.count(StudentModel.id))
                                         .where(StudentModel.room_id == room_id)) 
    except:
         return False, {"message":"Error fetching number of occupants in room (Catch)"}
    else:
        return  True,stud_in_room.scalar()




async def incre_update_room_status_given_room_id(room_obj:dict, session:async_sessionmaker):

    select_room_q = await session.execute(select(RoomModel).where(RoomModel.id == int(room_obj['id'])).with_for_update())
    select_room_res = select_room_q.scalar_one()
    if (int(select_room_res.capacity) - int(select_room_res.num_space_occupied)) == 1:
        select_room_res.num_space_occupied = select_room_res.num_space_occupied+1
        select_room_res.room_status = 'OCCUPIED'
        await incre_update_block_record_given_block_id_and_num_of_allocated_rooms(room_obj['block_id'],room_obj['num_rooms_in_block'],room_obj['num_of_allocated_rooms'],session)

    else:
        select_room_res.num_space_occupied = select_room_res.num_space_occupied+1
    

async def decre_update_room_status_given_room_id(room_id:int,space_id:int, session:async_sessionmaker):
    try:
        select_room_q = await session.execute(select(RoomModel).where(RoomModel.id == room_id).with_for_update())
        select_room_res = select_room_q.scalar_one()
        if select_room_res.room_status.value == "OCCUPIED":
            await decre_update_block_record_given_block_id(select_room_res.block_id,session)
        if select_room_res.num_space_occupied > 0:
            select_room_res.num_space_occupied = select_room_res.num_space_occupied-1
            select_room_res.room_status = 'AVAILABLE'
        else:
            return False, {"message":f"Non of the rooms in the block {select_room_res.room_name} was allocated to student before"}
        await session.execute(delete(StudentModel).where(StudentModel.id == space_id))
    except:
        return False,{"message":"Error removing student from room"}
    else:
        return True, {"message":"Student successfully removed from room"}



async def incre_update_block_record_given_block_id_and_num_of_allocated_rooms(block_id:int,num_rooms_in_block:int, num_of_allocated_rooms:int,session:async_sessionmaker):
    select_block = await session.execute(select(BlockModel).where(BlockModel.id == block_id).with_for_update())
    select_block = select_block.scalar_one()    
    if (int(select_block.num_rooms_in_block )- int(select_block.num_of_allocated_rooms)) == 1:
        select_block.num_of_allocated_rooms = select_block.num_of_allocated_rooms+1
        select_block.block_status = "OCCUPIED"
    else:
        select_block.num_of_allocated_rooms = select_block.num_of_allocated_rooms+1


async def decre_update_block_record_given_block_id(block_id:int, session:async_sessionmaker):
    try:
        select_block = await session.execute(select(BlockModel).where(BlockModel.id == block_id).with_for_update())
        select_block = select_block.scalar_one()
        if select_block.num_of_allocated_rooms > 0:
            select_block.num_of_allocated_rooms = select_block.num_of_allocated_rooms-1
            select_block.block_status = 'AVAILABLE'
        else:
            return False, {"message":f"Non of the rooms in the block {select_block.block_name} was allocated to student before"}
    except:
        return False,{"message":"Error executing Function decre_update_block_status_given_room_id "}
    else:
        return True, {"message":"Function decre_update_block_status_given_room_id successfully executed"}
   
   

async def default_query_db_for_random_available_room(stud_obj,session:async_sessionmaker):
  res =  await session.execute(select(RoomModel.id, RoomModel.room_name,RoomModel.capacity,RoomModel.num_space_occupied,BlockModel.block_name,BlockModel.num_rooms_in_block,
                                            BlockModel.num_of_allocated_rooms, BlockModel.gender,RoomModel.room_type, RoomModel.block_id,RoomModel.room_status,RoomModel.room_condition )
                                            .join(BlockModel, RoomModel.block_id == BlockModel.id)
                                            .where(RoomModel.room_status == "AVAILABLE")
                                            .where(BlockModel.block_status == "AVAILABLE")
                                            .where(BlockModel.gender == stud_obj['sex'])
                                            .with_for_update()
                                            .order_by(func.random())
                                            .limit(1))
  room = res.fetchone()
  if not room:
      return False, {"message":f"Is like no available room/block for gender {admin_service_helper1.get_full_gender_given_shortName(stud_obj['sex'])} in {stud_obj['curr_session']} academic session"}
  return True, room


async def query_db_for_random_available_room(stud_obj,session:async_sessionmaker):
  res =  await session.execute(select(RoomModel.id, RoomModel.room_name,RoomModel.capacity,RoomModel.num_space_occupied,BlockModel.block_name,BlockModel.num_rooms_in_block,
                                            BlockModel.num_of_allocated_rooms, BlockModel.gender,RoomModel.room_type, RoomModel.block_id,RoomModel.room_status,RoomModel.room_condition )
                                            .join(BlockModel, RoomModel.block_id == BlockModel.id)
                                            .where(RoomModel.room_status == "AVAILABLE")
                                            .where(BlockModel.block_status == "AVAILABLE")
                                            .where(BlockModel.gender == stud_obj['sex'])
                                            .where(BlockModel.proxy_to_portals_lodge == 'NO')
                                            .with_for_update()
                                            .order_by(func.random())
                                            .limit(1))
  room = res.fetchone()
  if not room:
      return False, {"message":f"Is like no available room/block for gender {admin_service_helper1.get_full_gender_given_shortName(stud_obj['sex'])} in {stud_obj['curr_session']} academic session"}
  return True, room


async def query_db_for_random_available_room_for_health_challenge_students(stud_obj,session:async_sessionmaker):
  res =  await session.execute(select(RoomModel.id, RoomModel.room_name,RoomModel.capacity,RoomModel.num_space_occupied,BlockModel.block_name,BlockModel.num_rooms_in_block,
                                            BlockModel.num_of_allocated_rooms, BlockModel.gender,RoomModel.room_type, RoomModel.block_id,RoomModel.room_status,RoomModel.room_condition )
                                            .join(BlockModel, RoomModel.block_id == BlockModel.id)
                                            .where(RoomModel.room_status == "AVAILABLE")
                                            .where(BlockModel.block_status == "AVAILABLE")
                                            .where(BlockModel.gender == stud_obj['sex'])
                                            .where(
                                                or_( BlockModel.proxy_to_portals_lodge == 'YES',
                                                    BlockModel.id.in_(select(BlockProximityToFacultyModel.block_id
                                                                            ).where(BlockProximityToFacultyModel.faculty == stud_obj['college_id']))
                                                    )
                                                
                                                )
                                            .with_for_update()
                                            .order_by(func.random())
                                            .limit(1))
  room = res.fetchone()
  if not room:
      res2 =  await session.execute(select(RoomModel.id, RoomModel.room_name,RoomModel.capacity,RoomModel.num_space_occupied,BlockModel.block_name,BlockModel.num_rooms_in_block,
                                            BlockModel.num_of_allocated_rooms, BlockModel.gender,RoomModel.room_type, RoomModel.block_id,RoomModel.room_status,RoomModel.room_condition )
                                            .join(BlockModel, RoomModel.block_id == BlockModel.id).where(RoomModel.room_status == "AVAILABLE")
                                            .where(BlockModel.block_status == "AVAILABLE").where(BlockModel.gender == stud_obj['sex'])
                                            .where(BlockModel.proxy_to_portals_lodge == 'YES')
                                            .with_for_update().order_by(func.random()).limit(1))
      alt_room = res2.fetchone()
      if not alt_room:
            return False, {"message":f"Is like no available room/block for gender {admin_service_helper1.get_full_gender_given_shortName(stud_obj['sex'])} in {stud_obj['curr_session']} academic session"}
      return True,alt_room  
  return True, room



async def query_db_for_random_available_room_with_faculty_proximity_condition(stud_obj,session:async_sessionmaker):
  res =  await session.execute(select(RoomModel.id, RoomModel.room_name,RoomModel.capacity,RoomModel.num_space_occupied,BlockModel.block_name,BlockModel.num_rooms_in_block,
                                            BlockModel.num_of_allocated_rooms, BlockModel.gender,RoomModel.room_type, RoomModel.block_id,RoomModel.room_status,RoomModel.room_condition )
                                            .join(BlockModel, RoomModel.block_id == BlockModel.id)
                                            .where(RoomModel.room_status == "AVAILABLE")
                                            .where(BlockModel.block_status == "AVAILABLE")
                                            .where(BlockModel.gender == stud_obj['sex'])
                                            .where(BlockModel.proxy_to_portals_lodge == 'NO')
                                            .where(BlockModel.id.in_(select(BlockProximityToFacultyModel.block_id).where(BlockProximityToFacultyModel.faculty == stud_obj['college_id'])))
                                            .with_for_update()
                                            .order_by(func.random())
                                            .limit(1))
  room = res.fetchone()
  if not room:
      return False, {"message":f"Is like no available room/block for gender {admin_service_helper1.get_full_gender_given_shortName(stud_obj['sex'])} in {stud_obj['curr_session']} academic session"}
  return True, room



async def  query_db_for_random_room_in_quest_house(stud_obj, session):
    res = await session.execute(select(RoomModel.id, RoomModel.room_name,RoomModel.capacity,RoomModel.num_space_occupied,BlockModel.block_name,BlockModel.num_rooms_in_block,
                                            BlockModel.num_of_allocated_rooms, BlockModel.gender,RoomModel.room_type, RoomModel.block_id,RoomModel.room_status,RoomModel.room_condition )
                                            .join(BlockModel, RoomModel.block_id == BlockModel.id)
                                            .where(RoomModel.room_status == "AVAILABLE")
                                            .where(BlockModel.block_status == "AVAILABLE")
                                            .where(BlockModel.id == 7)
                                            .where(BlockModel.gender == "F")
                                            .with_for_update()
                                            .order_by(func.random())
                                            .limit(1))
    room = res.fetchone()
    if not room:
      return False, {"message":f"Is like no available room in quest house in {stud_obj['curr_session']} academic session"}
    return True, room

 