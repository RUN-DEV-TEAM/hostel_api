import requests
from fastapi.responses import JSONResponse




def verify_supplied_email_from_staff_portal(email):
    response = requests.post(f'https://staff.run.edu.ng/auth_hostel_admin_user.php?req=verify&email={email}')
    if response.status_code == 200:
        res_data = response.json()
        if res_data["status"] == "ok":
            return True
        else:
            return False