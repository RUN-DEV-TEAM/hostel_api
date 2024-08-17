from datetime import datetime
from schemas.helperSchema import Gender


def check_for_norm_3_or_corn_4_room(room):
    pass

def build_response_dict(db_response, schema):
    response_dict = {}
    try:
        for field_name in schema.__fields__.keys():
            if  field_name == 'created_at' or field_name == 'updated_at':
                response_dict[field_name] = format_datetime(getattr(db_response, field_name))
            else:
                response_dict[field_name] = getattr(db_response, field_name)
    except KeyError:
        return False
    else:
        return response_dict
    

def format_datetime(dt: datetime) -> str:
    """
    Formats datetime to YYYY-MM-DDTHH:MM:SS format.
    """
    return dt.strftime('%Y-%m-%d %H:%M:%S')


# {'block_name': 'block 1', 'description': 'Rafiu Personal Statement', 'gender': <Gender.M: 'M'>, 
#  'num_rooms_in_block': 36, 'num_corn_rooms_in_block': 2, 
#  'corner_rooms': [{'value': 5, 'label': 'Room 5'}, {'value': 2, 'label': 'Room 2'}], 
#   'airy': True, 'water': True, 'num_norm_rooms_in_block': 0}

def validate_input_num_of_room_in_block(input:dict):
   print("#############################################@@@@@@@@@@@@@@@@@")
   print(input)
   msg = "Error from except... validating validate_input_num_of_room_in_block"
   try:
       num_rooms_in_block = int(input["num_rooms_in_block"])
       num_norm_rooms_in_block = int(input["num_norm_rooms_in_block"])
       num_corn_rooms_in_block = int(input["num_corn_rooms_in_block"])
       if num_rooms_in_block <= 0:
           msg = "Number of rooms in block cannot be 0"
           return False, msg
       if num_rooms_in_block != num_norm_rooms_in_block + num_corn_rooms_in_block:
           msg = "Number of rooms in block must be equal to sum of normal and corner rooms"
           return False, msg
   except:
       return False,msg
   else:
       msg = 'Success'
       return True,msg



def get_full_gender_given_shortName(gen):
    if gen == "F":
        return "Female"
    elif gen == "M":
        return "Male"
    else:
        return "Unkown gender"