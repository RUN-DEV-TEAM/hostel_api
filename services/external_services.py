import requests
from fastapi.responses import JSONResponse



def verify_supplied_email_from_staff_portal(email, password):
    try:
        response = requests.post(f'https://staff.run.edu.ng/auth_hostel_admin_user.php?hostel_to_staff=verify&email={email}&password={password}')
        if response.status_code == 200:
            res_data = response.json()
            if res_data["status"] == "ok":
                return True, {"message" : "User found on staff portal"}
            else:
                return False, {"message" : "Invalid Email/password, kindly provide correct email and passowrd as you have it on the staff portal"}
    except:
        return False, {"message" : "Error verifiying user from staff portal"}



# 

def get_current_academic_session():
    try:
        response = requests.post('https://nreg.run.edu.ng/apis/registration/getcurrentsession')
        if response.status_code == 200:
            res_data = response.json()
            return True, res_data['session']
        else:
            return False, {"message": "Can't get current session"}
    except:
        return False,{"message" : "Error get current session"}
    


def get_student_profile_in_session_given_matno(matno):
    try:
        response = requests.post(f'https://nreg.run.edu.ng/apis/profile/getstudent?matric={matno}')
        if response.status_code == 200:
            res_data = response.json()
            return True, res_data
        else:
            return False, {"message": f"No student profile found for matric number {matno}"}
    except:
        return False, {"message" : "Error fetching student profile"}
    


