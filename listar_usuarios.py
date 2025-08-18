import os
import json

from dotenv import load_dotenv

load_dotenv()


import importlib.util

spec = importlib.util.spec_from_file_location("hikvision_isapi", "./hikvision_isapi/client.py")
hikvision_C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hikvision_C)

hikvision_client = hikvision_C.HikvisionClient(
    base_url=os.getenv("HIK_URL", "http://192.168.8.25"),
    username=os.getenv("HIK_USERNAME", "admin"),
    password=os.getenv("HIK_PASSWORD", "admin2025"),
)


lista_users = hikvision_client.search_all_emps()

try:
    # connect to device
    #conn = zk.connect()
    # disable device, this method ensures no activity on the device while the process is run
    #conn.disable_device()
    # another commands will be here!
    # Example: Get All Users
    #users = conn.get_users()
    listausers = json.loads(lista_users.text)['UserInfoSearch']['UserInfo']
    print ('lista users')
    print (listausers)
    for user in listausers:
        privilege = 'User'
        #if user.privilege == const.USER_ADMIN:
        #    privilege = 'Admin'
        print ('=============')
        print (user)
        print ('emp ', user['employeeNo'])

        print ('+ EmployeeNo #{}'.format(user['employeeNo']))
        print ('  Name       : {}'.format(user['name']))
        print ('  User Type   : {}'.format(user['userType']))


    # Test Voice: Say Thank You
    #conn.test_voice()
    # re-enable device after all commands already executed
    #conn.enable_device()
except Exception as e:
    print ("Process terminate : {}".format(e))
finally:
    print ("TERMINOU......")
    #if conn:
    #    conn.disconnect()