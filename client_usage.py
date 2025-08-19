import os

from dotenv import load_dotenv

load_dotenv()

#from hikvision_isapi import HikvisionClient

#import sys
#sys.path.append('../hikvision_isapi')
#import hikvision_isapi
#from hikvision_isapi import HikvisionClient

import json
import importlib.util

spec = importlib.util.spec_from_file_location("hikvision_isapi", "./hikvision_isapi/client.py")
hikvision_C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hikvision_C)

'''
hikvision_client = HikvisionClient(
    base_url=os.getenv("HIK_URL", "http://192.168.8.25"),
    username=os.getenv("HIK_USERNAME", "admin"),
    password=os.getenv("HIK_PASSWORD", "admin2025"),
)
'''

hikvision_client = hikvision_C.HikvisionClient(
    base_url=os.getenv("HIK_URL", "http://192.168.8.25"),
    username=os.getenv("HIK_USERNAME", "admin"),
    password=os.getenv("HIK_PASSWORD", "admin2025"),
)

# res = hikvision_client.remote_control_door(door_id="1", command="close")
#res = hikvision_client.remote_control_door(door_id="1", command="alwaysOpen")
#print(res.status_code)
door = hikvision_client.get_door_capabilities()
print ('DOOR CAPA...')
print (door.status_code)
print (door.text)

cap = hikvision_client.get_access_control_capabilities()
print ('capabilities')
print (cap.status_code)
print (cap.text)

card = hikvision_client.get_card_status_capabilities()
print ('CARD Capabilities...')
print (card.status_code)



access = hikvision_client.get_access_events_capabilities()
print ('Access CAPABILKITIES......')
print (access.status_code)
print (access.text)

access = hikvision_client.get_access_events()
print ('Access Events...')
print (access.status_code)
print (access.text)

eventscap = hikvision_client.get_access_events_capabilities()
print ('Event Capabilietes.....')
print (eventscap.status_code)
print (eventscap.text)

eventscap = hikvision_client.get_access_events_total()
print ('Event Capabilietes.....')
print (eventscap.status_code)
print (eventscap.text)


users = hikvision_client.get_users_status_capabilities()
print ('USER.... cap')
print (users.status_code)
print (users.text)

users = hikvision_client.get_users()
print ('USER.... COUNT....')
print (users.status_code)
print (users.text)


deviceinfo = hikvision_client.get_device_info()
print ('DEvice INFO....')
print (deviceinfo.status_code)
print (deviceinfo.text)

novoUser = hikvision_client.create_user(empNo="1001",empName="Helio de Jesus")
print ('Creating... NEW USER')
print (novoUser.status_code)
print (novoUser.text)

setUser = hikvision_client.set_user(empNo="1001",empName="Helio  de Jesus")
print ('Change user Name or other details.....')
print (setUser.status_code)
print (setUser.text)

searchEmp = hikvision_client.search_emp(empNo="1001")
print ('Search for Emp....')
print (searchEmp.status_code)
print (searchEmp.text)

searchEmp = hikvision_client.search_all_emps()
print ('Search ALL Emp....')
print (searchEmp.status_code)
print (searchEmp.text)

'''
eventsHoje = hikvision_client.event_search()
print ('Eventos dia 15....')
print (eventsHoje.status_code)
print (eventsHoje.text)
'''

eventsHoje = hikvision_client.all_event_search()
print ('Eventos de HOJE....')
#print (eventsHoje.status_code)
print (eventsHoje)

'''
capab = hikvision_client.get_access_events_capabilities()
print ('cappppp')
print (capab.text)
'''