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
                if hasattr(db_response, field_name):
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




def validate_input_num_of_room_in_block(input:dict):
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


def strip_list_of_dict(list_data:dict):
    list_resp = []
    if isinstance(list_data, list):
        for item in list_data:
            list_resp.append(int(item['value']))
        return True,list_resp
    else:
        return False, {"message":"Wrong data type supplied ... not a list"}


def convert_true_false_to_yes_no(para:bool):
    if isinstance(para, bool):
        if para:
            return 'YES'
        elif not para:
            return 'NO'
        else:
            return 'NO'
    else:
        return False, {"message":"Wrong data type supplied ... not a boolean"}
    



def list_all_colleges():
    list_of_colleges = [
            {"college_id":"1","college":"HUMANITIES","last_updated_by":"bulk uploaded","last_updated_date":"2012-08-17"},
            {"college_id":"2","college":"MANAGEMENT SCIENCES","last_updated_by":"bulk uploaded","last_updated_date":"2012-08-17",},
            {"college_id":"3","college":"NATURAL SCIENCES","last_updated_by":"bulk uploaded","last_updated_date":"2012-08-17"},
            {"college_id":"4","college":"BASIC MEDICAL SCIENCES","last_updated_by":"bulk upload","last_updated_date":"2018-01-25"},
            {"college_id":"5","college":"LAW","last_updated_by":"","last_updated_date":"2019-06-01"},
            {"college_id":"6","college":"POSTGRADUATE STUDIES","last_updated_by":"teewhy","last_updated_date":"2020-03-05"},
            {"college_id":"7","college":"BUILT ENVIRONMENT STUDIES","last_updated_by":"teewhy","last_updated_date":"2020-03-05"},
            {"college_id":"8","college":"ENGINEERING","last_updated_by":"teewhy","last_updated_date":"2020-03-05"},
            {"college_id":"9","college":"SOCIAL SCIENCES","last_updated_by":"teewhy","last_updated_date":"2020-03-05"},
            {"college_id":"10","college":"EDUCATION","last_updated_by":"teewhy","last_updated_date":"2024-01-16"},
            {"college_id":"11","college":"DEST","last_updated_by":"teewhy","last_updated_date":"2024-01-16"},
             {"college_id":"12","college":"ADMIN","last_updated_by":"teewhy","last_updated_date":"2024-01-16"},
             {"college_id":"13","college":"ALL","last_updated_by":"teewhy","last_updated_date":"2024-01-16"},
             {"college_id":"14","college":"GUEST HOUSE","last_updated_by":"teewhy","last_updated_date":"2024-01-16"},

            ]
    return list_of_colleges



def list_of_matric_number_with_health_issue(matno:str):
    matno = str(matno).split("/")[-1]
    list_mat = ['8730','143','13302','14302', '15554', '14603','340','14684','14988','15372','14338','14209','15460','14991','15778','13712','13431','13573','13419','10358','9615','11279','9105','151',
                '12756','10899','13113','13564','12197','7957','10153','15776','9797','9180','10525','15803','11747','11666','12232','11934','8750','123','10716','10735','12597','12671','14440','14970','9307','9310','10025','11599','11659','11660','11570','10761','10820','12024','12818','12895','12988','15360','10330','11084','12129','10477','12244','039',
                '161','188','10515','12264','12273','14753','8368','10640','14843','14866','14918','9206','9241','13441','13222','13223','13229','13232','13257','13258','11221','11270','13401','13415','13586','13615','15596','15663','9679','9744','9763','14162','10102',
                '11740','11753','14319','7213','7929','8742','8781','11844','14117','10276','8857','8844','8873','13295','13636','13648','13656','9607','11040','13686','15805','15813','15814','15819','15823','11910','11918','14384','11996','11059','11213','15836','10619',
                '10622','12476','14802','9172','9376','13719','15702','15379','15850','14830','126','15525','15040','12789','15547','11991','12216','15136','9729','9756','14804','15097','15125','9447','12414','10157','14156','12716','9279','10362','12077','12416','8242','13595','13606','8883','10596','10327','12641','8284','14543','13089','14884',
                '10399','15062','14132','8716','14640','9194','11199','13505','9684','14555','14163','14415','14889','14352','15010','15036','15183','15184','15063','14884','14479','15427','14754','15718','15286','15097','14951','14543','14825','15349','15473','14684','14517','15796','14395','14050']
    if matno in list_mat:
        return "YES"
    return 'NO'



# Note 2024/2025 is meant final year female student
def check_eligibility_for_female_guest_house(stud_obj):
    try:
        return True
        # if stud_obj['level'] in ['400', '500', '600']:
        #     if stud_obj['program_code'] in ["BDG","CHE","CPE","CVE","EEE","ESM","LAW","MEE","MLS","NUR","PHT","QSV","SGI","URP"] and str(stud_obj['level']) == '400':
        #         return False
        #     return True
        # else:
        #     return False
    except:
        return False