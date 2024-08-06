from datetime import datetime
from sqlalchemy import func,update, and_
from models.userModel import RoomModel,StudentModel,BlockModel
from schemas.studentSchema import StudentRoomSchema
from schemas.roomSchema import RoomSchemaDetailed,RoomAllocationResponseSchema
from schemas.helperSchema import Gender
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.future import select
from services import admin_service_helper1



async def get_student_room_in_session(mat_no:str,curr_session:str, session:async_sessionmaker):
   result = await session.execute(select(StudentModel.id,StudentModel.matric_number,StudentModel.room_id,StudentModel.acad_session,
                                         StudentModel.deleted,StudentModel.created_at,StudentModel.updated_at
                                         ).where(StudentModel.matric_number == str(mat_no).strip(),
                                                             StudentModel.acad_session == str(curr_session).strip()))
   stud_room = result.fetchone()  
   if not stud_room:
       return False, {"message":f"No room for matric number {mat_no}"}
   stud_room_dict = admin_service_helper1.build_response_dict(stud_room,StudentRoomSchema)
   room_details = await get_room_details_given_student_room_id(stud_room_dict['room_id'],session)
   if room_details[0]:
       stud_room_dict.update({"room_details":room_details[1]})
   return True, stud_room_dict



async def get_random_available_room(gender:Gender,curr_session:str, session:async_sessionmaker):
    get_room = await session.execute(select(RoomModel.id, RoomModel.rooms_name,RoomModel.capacity,BlockModel.block_name,BlockModel.num_rooms_in_block,
                                           BlockModel.num_of_allocated_rooms, BlockModel.gender,RoomModel.room_type, RoomModel.block_id,RoomModel.room_status,RoomModel.room_condition )
                                        .join(BlockModel, RoomModel.block_id == BlockModel.id)
                                        .where(RoomModel.room_status == "AVAILABLE")
                                        .where(BlockModel.block_status == "AVAILABLE")
                                        .where(BlockModel.gender == gender)
                                        .with_for_update()
                                        .order_by(func.random())
                                        .limit(1))
    
    room = get_room.fetchone()
    if not room:
       return False, {"message":f"Is like no available room/block for gender {admin_service_helper1.get_full_gender_given_shortName(gender)} in {curr_session} academic session"}
    return True, admin_service_helper1.build_response_dict(room,RoomSchemaDetailed)



async def get_specific_available_room_in_block(gender:Gender,curr_session:str, block_id:int,session:async_sessionmaker):
    get_room = await session.execute(select(RoomModel.id, RoomModel.rooms_name,RoomModel.capacity,BlockModel.block_name,BlockModel.num_rooms_in_block,
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



async def get_specific_available_space_in_room(gender:Gender,curr_session:str, room_id:int,session:async_sessionmaker):
    get_room = await session.execute(select(RoomModel.id, RoomModel.rooms_name,RoomModel.capacity,BlockModel.block_name,BlockModel.num_rooms_in_block,
                                           BlockModel.num_of_allocated_rooms, BlockModel.gender,RoomModel.room_type, RoomModel.block_id,RoomModel.room_status,RoomModel.room_condition )
                                        .join(BlockModel, RoomModel.block_id == BlockModel.id)
                                        .where(RoomModel.room_status == "AVAILABLE")
                                        .where(BlockModel.block_status == "AVAILABLE")
                                        .where(BlockModel.gender == gender)
                                        .where(RoomModel.id == room_id)
                                        .with_for_update()
                                        .order_by(func.random())
                                        .limit(1))
    
    room = get_room.fetchone()
    if not room:
       return False, {"message":f"Is like no available room/block for gender {admin_service_helper1.get_full_gender_given_shortName(gender)} in {curr_session} academic session"}
    return True, admin_service_helper1.build_response_dict(room,RoomSchemaDetailed)

 
    
async def room_allocation_service(matric_number:str,room_id:int,block_id:int,num_rooms_in_block:int,
                                  num_of_allocated_rooms:int,acad_session:str,room_capacity:int,session:async_sessionmaker):
    try:
        _allo_room = StudentModel(matric_number=matric_number,room_id=room_id,acad_session=acad_session)
        session.add(_allo_room)
        no_stud_in_room = await get_number_of_occupant_in_room(room_id,session)
        if no_stud_in_room[0]:
            if (room_capacity - int(no_stud_in_room[1]) ) == 1:
                await update_room_status_given_room_id(room_id, session)
        await update_block_record_given_block_id_and_num_of_allocated_rooms(block_id,num_rooms_in_block,num_of_allocated_rooms,session)
        await session.commit()
        await session.refresh(_allo_room)
        room_dict = admin_service_helper1.build_response_dict(_allo_room,RoomAllocationResponseSchema)
        room_details = await get_room_details_given_student_room_id(room_id,session)
        if room_details[0]:
            room_dict.update({"room_details":room_details[1]})
        return True,room_dict
    except:
        return False, {"message":"Error allocating room"}




async def get_room_details_given_student_room_id(room_id:int, session:async_sessionmaker):
        room_details = await session.execute(select(RoomModel.id, RoomModel.rooms_name,RoomModel.capacity,BlockModel.block_name,
                                                    BlockModel.num_rooms_in_block,BlockModel.num_of_allocated_rooms,BlockModel.gender,
                                                RoomModel.room_type, RoomModel.block_id,RoomModel.room_status,RoomModel.room_condition   
                                       )
                                        .join(BlockModel, RoomModel.block_id == BlockModel.id)
                                        .where(RoomModel.id == room_id)
                                        .limit(1))
    
        room_details = room_details.fetchone()
        if not room_details:
            return False, {"message":f"Like no room is foind with the supplied id ::: {room_id}"}
        return True, admin_service_helper1.build_response_dict(room_details,RoomSchemaDetailed)
   


async def get_number_of_occupant_in_room(room_id:int, session:async_sessionmaker):
    try:
        stud_in_room = await session.execute(select(func.count(StudentModel.id))
                                         .where(StudentModel.room_id == room_id)) 
    except:
         return False, {"message":"Error fetching number of occupants in room (Catch)"}
    else:
        return  True,stud_in_room.scalar()




async def update_room_status_given_room_id(room_id:int, session:async_sessionmaker):
    await session.execute(update(RoomModel).where(RoomModel.id == room_id).values(room_status="OCCUPIED")
                                 .execution_options(synchronize_session="fetch"))


async def update_block_record_given_block_id_and_num_of_allocated_rooms(block_id:int,num_rooms_in_block:int, num_of_allocated_rooms:int,session:async_sessionmaker):
    if (num_rooms_in_block - num_of_allocated_rooms) == 1:
        await session.execute(update(BlockModel).where(BlockModel.id == block_id)
                              .values(block_status="OCCUPIED", num_of_allocated_rooms= num_of_allocated_rooms+1)
                                 .execution_options(synchronize_session="fetch"))
    else:
        await session.execute(update(BlockModel).where(BlockModel.id == block_id)
                              .values(num_of_allocated_rooms= num_of_allocated_rooms+1)
                                 .execution_options(synchronize_session="fetch"))
   
   
   
    #  matric_number = Column(String(65), nullable=False)
    # room_id = Column(Integer, ForeignKey('t_rooms.id'), nullable=False)
    # acad_session = Column(String(9), nullable=False)
    # deleted = Column(Enum(Deleted), default=Deleted.N)
    # created_at = Column(DateTime, server_default= text('CURRENT_TIMESTAMP'))
    # updated_at = Column(DateTime, default=func.now(), onupdate=func.now())