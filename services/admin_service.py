from typing import List
from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy import func,distinct
from models.userModel import UserModel,BlockModel,RoomModel,StudentModel,BlockProximityToFacultyModel
from schemas.userSchema import CreateUser,ListUser,ReturnSignUpUser,ListUser2
from schemas.blockSchemas import BlockSchema,GetRoomStat,BlockRoomSchema2,BlockSchemaCreate,BlockRoomSchema,BlockProxityResponse,ListAllBlockSchemeResponse
from schemas.roomSchema import RoomSchema,RoomSchemaDetailed,RoomStatusSchema,RoomSchemaWithOutBlockName
from schemas.studentSchema import ListStudentInRoomSchema,StudentInBlockchema,ListAllOccupantSchemaResponse
from schemas.helperSchema import Gender,RoomCondition
from services import admin_service_helper1
from services import admin_service_helper2
from api.endpoints import endpoint_helper
from services import external_services
from sqlalchemy.ext.asyncio import async_sessionmaker



async def sign_up_service(user_create:CreateUser, session:async_sessionmaker) -> ListUser:
   user_create = user_create.model_dump()
   status,data = external_services.verify_supplied_email_from_staff_portal(user_create["email"],user_create["password"])
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
  


async def create_new_block_db_service(input:BlockSchemaCreate, session:async_sessionmaker):
    try:
        block = input.model_dump()
        if isinstance(block['corner_rooms'], str):
            block.update({"num_norm_rooms_in_block":block['num_rooms_in_block'],"num_corn_rooms_in_block":0})
        num_norm_rooms_in_block = int(block['num_rooms_in_block']) - int(block['num_corn_rooms_in_block']) 
        block.update({"num_norm_rooms_in_block":num_norm_rooms_in_block})
        if not admin_service_helper1.validate_input_num_of_room_in_block(block)[0]:
            return False,{"message":admin_service_helper1.validate_input_num_of_room_in_block(block)[1]} 
        block_model_inst = BlockModel(block_name=block['block_name'] , description= block['description'], 
                                        gender=block['gender'] ,num_rooms_in_block= block['num_rooms_in_block'],
                            num_norm_rooms_in_block= block['num_norm_rooms_in_block'],num_corn_rooms_in_block= block['num_corn_rooms_in_block'],
                            airy= admin_service_helper1.convert_true_false_to_yes_no(block['airy']),
                            water_access=admin_service_helper1.convert_true_false_to_yes_no(block['water']),proxy_to_portals_lodge=admin_service_helper1.convert_true_false_to_yes_no(block['access_to_lodge']))
        session.add(block_model_inst)
        await session.commit()
        await session.refresh(block_model_inst)
        if admin_service_helper1.strip_list_of_dict(block['block_access_to_fac'])[0]:
            block_fac_access_stripped = admin_service_helper1.strip_list_of_dict(block['block_access_to_fac'])[1]
            block_proxi = [BlockProximityToFacultyModel(faculty=el, block_id=block_model_inst.id) for el in block_fac_access_stripped]
            session.add_all(block_proxi)
            await session.commit()
        list_room_num = [num for num in range(1, int(block['num_rooms_in_block'])+1)]
        if admin_service_helper1.strip_list_of_dict(block['corner_rooms'])[0]:
            corn_room_stripped = admin_service_helper1.strip_list_of_dict(block['corner_rooms'])[1]
            list_of_norm_room_num = [norm for norm in list_room_num if norm not in corn_room_stripped]
        norm_room_objs = [RoomModel(room_name= f"room {i}",capacity=block['norm_room_capacity'], room_type="NORMAL",block_id = block_model_inst.id) 
                                for i in list_of_norm_room_num]
        session.add_all(norm_room_objs)
        await session.commit()
        if len(corn_room_stripped)>0 and block['num_corn_rooms_in_block'] >0 and (int(num_norm_rooms_in_block) < int(block['num_rooms_in_block'])):
            corn_room_objs = [RoomModel(room_name= f"room {i}",capacity=block['corn_room_capacity'], room_type="CORNER",block_id = block_model_inst.id) 
                                    for i in corn_room_stripped]
            session.add_all(corn_room_objs)
            await session.commit()
    except:
         await session.rollback()
         return False,{"message":"Error creating block and rooms"} 
    else:
        block_dict = admin_service_helper1.build_response_dict(block_model_inst,BlockSchema) 
        list_norm_rooms_created = [admin_service_helper1.build_response_dict(norm_obj,RoomSchemaWithOutBlockName)  for norm_obj in norm_room_objs ]
        list_corn_rooms_created = [admin_service_helper1.build_response_dict(corn_obj,RoomSchemaWithOutBlockName)  for corn_obj in corn_room_objs ]
        list_block_fac_access_stripped = [admin_service_helper1.build_response_dict(obj,BlockProxityResponse)  for obj in block_proxi]
        block_dict.update({"norm_room":list_norm_rooms_created, "corner_room":list_corn_rooms_created, "block_access_to_fac":list_block_fac_access_stripped})
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



async def get_all_available_rooms_from_selected_block_service(block_id:int, session:async_sessionmaker):
   try:
       result = await session.execute(select(RoomModel.id, RoomModel.room_name,RoomModel.capacity,
                                       RoomModel.room_type, RoomModel.block_id,BlockModel.block_name,RoomModel.room_status,RoomModel.room_condition   
                                       )
                                       .join(BlockModel, RoomModel.block_id == BlockModel.id)
                                       .where(RoomModel.block_id == block_id,RoomModel.room_status =='AVAILABLE',RoomModel.room_condition =='GOOD',RoomModel.deleted == 'N'))
       room_list = result.all()
       resp = [admin_service_helper1.build_response_dict(room,RoomSchema)  for room in room_list]
   except:
       return False, {"message":f"Error fetching all available rooms in block given block ID {block_id}"}
   else:
       return True,resp



async def get_all_occupied_rooms_from_selected_block_service(block_id:int, session:async_sessionmaker):
   try:
        result = await session.execute(select(RoomModel.id, RoomModel.room_name,RoomModel.capacity,
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


async def get_stud_profile_and_randomly_assign_room_to_student_in_session_service(mat_no, session):
    mat_no = str(mat_no).strip()
    stud_profile =  external_services.get_student_profile_in_session_given_matno(mat_no)
    curr_session = external_services.get_current_academic_session()
    if stud_profile[0] and curr_session[0]:
        stud_obj = stud_profile[1]
        stud_obj['matric_number'] = mat_no
        stud_obj['curr_session'] = curr_session[1]
        res = await first_condition_before_ramdom_room_allocation(stud_obj,session)
        if res[0]:
            return True,res[1]
        else:
            return False,res[1]
    else:
        return False,stud_profile[1]
    

async def random_assign_room_to_student_in_session_service(in_data:dict,get_room_condition:dict, session:async_sessionmaker):
    check_for_stud_room = await admin_service_helper2.get_student_room_in_session(in_data,session)
    if not check_for_stud_room[0]:
        get_room = await admin_service_helper2.get_random_available_room(in_data,get_room_condition,session)
        if get_room[0]:
            allo_room = await admin_service_helper2.room_allocation_service(in_data,get_room[1],session)
            if allo_room:
                return True,allo_room[1]
        else:
            return False, get_room[1] 
    else:
        return True, check_for_stud_room[1]
    


async def assign_room_in_specific_block_to_student_in_session_service(mat_no:str,block_id:int, session:async_sessionmaker):
    stud_profile =  external_services.get_student_profile_in_session_given_matno(mat_no)
    curr_session = external_services.get_current_academic_session()
    if stud_profile[0] and curr_session[0]:
        stud_obj = stud_profile[1] 
        stud_obj['matric_number'] = mat_no
        stud_obj['curr_session'] = curr_session[1]
        check_for_stud_room = await admin_service_helper2.get_student_room_in_session(stud_obj,session)
        if not check_for_stud_room[0]:
            get_room = await admin_service_helper2.get_specific_available_room_in_block(stud_obj["sex"], curr_session[1],block_id,session)
            if get_room[0]:
                allo_room = await admin_service_helper2.room_allocation_service(stud_obj,get_room[1],session)
                if allo_room:
                    return True,allo_room[1]
            else:
                return False, get_room[1] 
        else:
            return True, check_for_stud_room[1]
    else:
        return False,stud_profile[1]


async def first_condition_before_ramdom_room_allocation(stud_obj,session):

    if not stud_obj['accom_payable'] or not stud_obj['special_accom_payable']:
        return False,{"message":"Issue with datatype field ...accom_payable or special_accom_payable"}    
    if int(stud_obj['accom_paid']) < int(stud_obj['accom_payable']) :
            return False, {"message": f"#{stud_obj['accom_payable']}  is the amount payable for accommodation but you have just paid #{int(stud_obj['accom_paid'])}"}
    elif int(stud_obj['accom_paid']) >= int(stud_obj['accom_payable']) :      
        get_room_condition = {'room_cat':''}
        if (int(stud_obj['special_accom_paid']) >= int(stud_obj['special_accom_payable'])) and int(stud_obj['special_accom_paid']) > 0:
            get_room_condition['room_cat'] = 'SPECIAL'
            print(stud_obj)         
            res = await random_assign_room_to_student_in_session_service(stud_obj,get_room_condition,session)
            if res[0]:
                return True, res[1]
            else:
                return False, res[1]
        elif int(stud_obj['special_accom_paid']) == -1 and (int(stud_obj['accom_paid']) >= int(stud_obj['accom_payable']) ):
            get_room_condition['room_cat'] = 'GENERAL'           
            res = await random_assign_room_to_student_in_session_service(stud_obj,get_room_condition,session)
            if res[0]:
                return True, res[1]
            else:
                return False, res[1]
        else:
            return False,{"message":"Ops!! I doubt if you have actually paid minimum requirement for accommodation in this session"}
    else:
        return False,{"message":"Sorry!! Your acclaimed payment for accommodation can not be verified now"}    



async def assign_specific_space_in_room_to_student_in_session_service(mat_no:str,room_id:int, session:async_sessionmaker):
    stud_profile =  external_services.get_student_profile_in_session_given_matno(mat_no)
    curr_session = external_services.get_current_academic_session()
    if stud_profile[0] and curr_session[0]:
        stud_obj = stud_profile[1] 
        stud_obj['matric_number'] = mat_no
        stud_obj['curr_session'] = curr_session[1]
        check_for_stud_room = await admin_service_helper2.get_student_room_in_session(stud_obj,session)
        if not check_for_stud_room[0]:
            get_room = await admin_service_helper2.get_specific_available_space_in_room(stud_obj,room_id,session)
            if get_room[0]:
                allo_room = await admin_service_helper2.room_allocation_service(stud_obj,get_room[1],session)
                if allo_room:
                    return True,allo_room[1]
            else:
                return False, get_room[1] 
        else:
            return True, check_for_stud_room[1]
    else:
        return False,stud_profile[1]


async def get_student_room_in_session_service(mat_no:str,session_id:str, session:async_sessionmaker):
    stud_obj = {"matric_number":mat_no, "curr_session":session_id}
    stud_room = await admin_service_helper2.get_student_room_in_session(stud_obj,session)
    if not stud_room[0]:
        return False, stud_room[1]
    else:
        return True,stud_room[1]


async def delete_student_from_room_in_session_service(mat_no:str,session_id:str, session:async_sessionmaker):
     stud_obj = {"matric_number":mat_no, "curr_session":session_id}
     stud_room = await admin_service_helper2.get_student_room_in_session(stud_obj,session)
     if stud_room[0]:
         await admin_service_helper2.decre_update_block_record_given_block_id(stud_room[1]['room_details']['block_id'],session)
         res = await admin_service_helper2.decre_update_room_status_given_room_id(stud_room[1]['room_details']['id'],stud_room[1]['id'],session)
         await session.commit()
         return True,res[1]
     else:
         return False, stud_room[1]



async def list_student_in_room_in_session_service(room_id:int, session:async_sessionmaker):
    try:
        stud_in_room = await session.execute(select(StudentModel.id,StudentModel.matric_number,StudentModel.surname,
                                                   StudentModel.firstname, StudentModel.sex, StudentModel.level,
                                                   StudentModel.program,StudentModel.dpt ,StudentModel.college,
                                                    StudentModel.room_id,
                                                    StudentModel.curr_session,StudentModel.deleted,StudentModel.created_at,StudentModel.updated_at)
                                    .where(StudentModel.room_id == room_id))
        result =  stud_in_room.all()
        if result:
            resp = [admin_service_helper1.build_response_dict(room,ListStudentInRoomSchema)  for room in result]
            return True,resp
        else:
            return False, {"message":"No student allocated to this room yet"}
    except:
        return False, {"message":f"Error fetching students in the room with id {room_id}"}



async def get_room_status_in_session_service(room_id:int, session:async_sessionmaker):
    try:
        query = await session.execute(select(RoomModel.id,RoomModel.room_name,RoomModel.capacity,RoomModel.room_type,
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



async def list_rooms_with_empty_space_in_session_service(gender:Gender, session:async_sessionmaker):
    try:
        # query = await session.execute(select(distinct(StudentModel.room_id)).where(StudentModel.acad_session==session_id))
        # list_occupied_room_in_session_id = query.scalars().all()
        curr_session = external_services.get_current_academic_session()
        if  curr_session[0]:
            get_room = await session.execute(select(RoomModel.id, RoomModel.room_name,RoomModel.capacity,BlockModel.block_name,BlockModel.num_rooms_in_block,
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
        else:
            return False,curr_session[1]
    except:
        return False, {"message":"Database error fetching list_rooms_with_empty_space_in_session_service"}



async def list_occupied_rooms_in_session_service(gender:Gender, session:async_sessionmaker):
    try:
        get_room = await session.execute(select(RoomModel.id, RoomModel.room_name,RoomModel.capacity,BlockModel.block_name,
                                              BlockModel.description,  BlockModel.num_rooms_in_block,
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
 

# 

async def list_occupied_blocks_in_session_service(gender:Gender, session:async_sessionmaker):
    try:
        get_block = await session.execute(select(BlockModel.id,BlockModel.block_name,BlockModel.description,BlockModel.gender,BlockModel.block_status,
                                                BlockModel.num_rooms_in_block,BlockModel.num_of_allocated_rooms,
                                                BlockModel.num_norm_rooms_in_block, BlockModel.num_corn_rooms_in_block,
                                                BlockModel.created_at,BlockModel.updated_at, BlockModel.deleted)
                                            .where(BlockModel.block_status == "OCCUPIED")
                                            .where(BlockModel.gender == gender))
        blocks =  get_block.all()
        if not blocks:
            return False, {"message":"No block is occupied in session ..."}
        format_data = [admin_service_helper1.build_response_dict(block,BlockRoomSchema2) for block in blocks ]
        return True, format_data
    except:
        return False, {"message":"Database error fetching list_blocks_with_empty_rooms_in_session_service"}



async def list_students_with_accomodation_in_block_in_session_service(block_id:int,  session:async_sessionmaker):
    try:
        query = await session.execute(select(StudentModel.id, StudentModel.matric_number,StudentModel.surname,
                                             StudentModel.firstname,StudentModel.level,StudentModel.program,
                                             StudentModel.dpt,StudentModel.college,StudentModel.curr_session,
                                            StudentModel.room_id,StudentModel.created_at, StudentModel.updated_at,
                                            RoomModel.room_name, RoomModel.capacity,RoomModel.room_type,RoomModel.room_status,RoomModel.room_condition,
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



async def list_students_with_accomodation_in_session_given_gender_service(gender:str, session:async_sessionmaker):
        curr_session = external_services.get_current_academic_session()
        if curr_session[0]:
            query = await session.execute(select(StudentModel.id, StudentModel.matric_number,StudentModel.surname,StudentModel.firstname,
                                                StudentModel.curr_session,StudentModel.program,StudentModel.college,
                                                StudentModel.room_id,StudentModel.created_at, StudentModel.updated_at,
                                                RoomModel.room_name, RoomModel.capacity,RoomModel.room_type,RoomModel.room_status,RoomModel.room_condition,
                                                BlockModel.block_name,BlockModel.gender,BlockModel.description)
                                                .join(RoomModel, StudentModel.room_id == RoomModel.id)
                                                .join(BlockModel, RoomModel.block_id == BlockModel.id )
                                                .where(BlockModel.gender  == gender)
                                                .where(StudentModel.curr_session  == curr_session[1]))
            studs = query.all()
            if not studs:
                    return False, {"message":f"No occupant(s) found for  ... in {curr_session[1]}"}
            format_data = [admin_service_helper1.build_response_dict(stud,ListAllOccupantSchemaResponse) for stud in studs ]
            return True, format_data   
        else:
            return False, curr_session[1]
 
 

async def list_all_available_blocks_given_gender_service(gender:str, session:async_sessionmaker):
    
        query = await session.execute(select(BlockModel.id, BlockModel.block_name,BlockModel.description, BlockModel.gender,BlockModel.num_norm_rooms_in_block,
                                             BlockModel.num_of_allocated_rooms, BlockModel.num_rooms_in_block,
                                             BlockModel.num_corn_rooms_in_block, BlockModel.block_status, 
                                             BlockModel.airy, BlockModel.water_access, BlockModel.proxy_to_portals_lodge, BlockModel.created_at)
                                            .where(BlockModel.gender  == gender))
        studs = query.all()
        if not studs:
                return False, {"message":f"No Block found..."}
        format_data = [admin_service_helper1.build_response_dict(stud,ListAllBlockSchemeResponse) for stud in studs ]
        return True, format_data   
      


def list_all_colleges_service():
    res = admin_service_helper1.list_all_colleges()
    if res:
        return True, res
    else:
        return False, {"message":"Can't fetch college(s) at the moment"}
    # 
# NOTE:  fetchone() vs scalar_one()
# .where(RoomModel.id.notin_(list_occupied_room_in_session_id))