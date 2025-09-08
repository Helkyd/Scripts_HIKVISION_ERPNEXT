#Last Modified 22-08-2025
import logging
import os
from typing import Literal

import requests
from requests.auth import HTTPDigestAuth
from requests.exceptions import HTTPError

#FIX 08-09-2025
from datetime import datetime, date, timedelta
import time


class HikvisionHeadersTemplate:
    DEFAULT = None
    REQ_XML = {
        "Content-Type": "application/xml",
    }


class HikvisionClient:
    def __init__(
        self,
        base_url: str,
        username: str,
        password: str,
        verify_ssl: bool = True,
    ) -> None:
        self.logger = logging.getLogger(__name__)
        if "" in [base_url, username, password]:
            raise ValueError(
                "Vars not configured correctly. "
                f"Base URL: {base_url}, username: {username}, password: {password}."
            )
        self.username = username
        self.password = password
        self.base_url = base_url.strip("/")
        self.headers_template = {""}
        self.verify_ssl = verify_ssl
        if os.environ.get("VERIFY_SSL", "True").lower() != "true":
            self.verify_ssl = False

    def _generate_auth(self) -> HTTPDigestAuth:
        return HTTPDigestAuth(username=self.username, password=self.password)

    def request(
        self,
        path: str,
        method="GET",
        headers=HikvisionHeadersTemplate.DEFAULT,
        data=None,
        json=None,
    ):
        url = self.base_url + path
        self.logger.debug(
            f"Requesting to url: {url}, method: {method}, "
            f"data: {data}, json: {json}"
        )
        res = requests.request(
            method=method,
            headers=headers,
            auth=self._generate_auth(),
            url=url,
            data=data,
            json=json,
            verify=self.verify_ssl,
        )
        # self.logger.debug(res.request.headers)
        # try:
        #     res.raise_for_status()
        # except HTTPError as err:
        #     self.logger.error(
        #         f"Requesting to url: {url}, method: {method}, "
        #         f"data: {data}, json: {json}"
        #     )
        #     raise err
        return res

    def get_access_control_capabilities(self):
        res = self.request(
            method="GET",
            path="/ISAPI/AccessControl/capabilities",
        )
        return res

    def get_door_capabilities(self):
        res = self.request(
            method="GET",
            path="/ISAPI/AccessControl/RemoteControl/door/capabilities",
        )
        return res

    def remote_control_door(
        self,
        door_id: str,
        command: Literal["open", "close", "alwaysOpen", "alwaysClose"],
    ):
        door_data_template = (
            f"<RemoteControlDoor><cmd>{command}</cmd></RemoteControlDoor>"
        )
        res = self.request(
            method="PUT",
            path=f"/ISAPI/AccessControl/RemoteControl/door/{door_id}",
            headers=HikvisionHeadersTemplate.REQ_XML,
            data=door_data_template,
        )
        self.logger.debug(
            f"Remote control res: {res.status_code} | {res.headers} | {res.text}"
        )
        return res

    def get_door_security_module_status_capabilities(self):
        res = self.request(
            method="GET",
            path="/ISAPI/AccessControl/RemoteControl/door/capabilities",
        )
        return res

    def get_card_status_capabilities(self):
        print ('Chamou get card status capabilities...')
        res = self.request(
            method="GET",
            path="/ISAPI/AccessControl/CardInfo/capabilities?format=json",
        )
        return res

    def get_users_status_capabilities(self):
        print ('get users capabilies...')
        res = self.request(
            method="GET",
            path="/ISAPI/AccessControl/UserInfo/capabilities?format=json",
        )
        return res
    
    def get_users(self):
        print ('get users CAOUNT......')
        res = self.request(
            method="POST",
            path="/ISAPI/AccessControl/UserInfo/Search?format=json",

        )
        return res
    
    def get_access_events_capabilities(self):
        print ('Get Access Events')
        res = self.request(
            method="GET",
            path="/ISAPI/AccessControl/AcsEvent/capabilities?format=json",
        )
        return res
    
    def get_access_events(self):
        print ('Get Access Events')
        res = self.request(
            method="GET",
            path="/ISAPI/AccessControl/AcsEvent?format=json",
            json={"AcsEventCond":{"searchID":"40e4ccc6-d819-4a57-b5fa-10591c9997d8","searchResultPosition":0,"maxResults":10,"major":5,"startTime":"2025-01-27T08:44:18\u002B00:00","endTime":"2025-01-28T08:44:18\u002B00:00"}},
        )
        return res
    
    def get_access_events_capabilities(self):
        print ('Get Access Events CAPABILIETES.....')
        res = self.request(
            method="GET",
            path="/ISAPI/AccessControl/AcsEventTotalNum/capabilities?format=json",

        )
        return res

    def get_access_events_total(self):
        print ('Get Access Events TOTAL.....')
        res = self.request(
            method="GET",
            path="/ISAPI/AccessControl/AcsEventTotalNum?format=json",

        )
        return res
    
    def get_device_info(self):
        print ('DEVICE INFO.....')
        res = self.request(
            method="GET",
            path="/ISAPI/System/deviceInfo",
            #path="/ISAPI/System/capabilities?format=json",
        )
        return res
    
    def create_user(self,empNo,empName,):
        print ('Creating new user on FINGERPRINT....')
        newuser = {"UserInfo": {
                "employeeNo": empNo,
                "name": empName,
                "userType": "normal",
                "Valid": {
                "enable": True,
                "beginTime": "2025-01-01T00:00:00",
                "endTime": "2030-01-01T00:00:00"
                },
                "doorRight": "1",
                "RightPlan": [
                {
                    "doorNo": 1,
                    "planTemplateNo": "1"
                }
                ]
            }
        }
        res = self.request(
            method="POST",
            path="/ISAPI/AccessControl/UserInfo/Record?format=json",
            json=newuser,
        )
        return res
    
    
    def set_user(self,empNo,empName,):
        print ('Set user on FINGERPRINT....')
        newuser = {"UserInfo": {
                "employeeNo": empNo,
                "name": empName,
                "userType": "normal",
                "Valid": {
                "enable": True,
                "beginTime": "2025-01-01T00:00:00",
                "endTime": "2030-01-01T00:00:00"
                },
                "doorRight": "1",
                "RightPlan": [
                {
                    "doorNo": 1,
                    "planTemplateNo": "1"
                }
                ]
            }
        }
        res = self.request(
            method="PUT",
            path="/ISAPI/AccessControl/UserInfo/SetUp?format=json",
            json=newuser,
        )
        return res

    def search_emp(self,empNo):
        print ('Search for Employeee....')
        searchemp = {"UserInfoSearchCond": {
                "searchID": "1",
                "searchResultPosition": 0,
                "maxResults": 30,
                "EmployeeNoList":[{"employeeNo":empNo}]
            }
        }
        res = self.request(
            method="POST",
            path="/ISAPI/AccessControl/UserInfo/Search?format=json",
            json=searchemp,
        )
        return res
    
    def search_all_emps(self):
        print ('Search ALL Employeee....')
        searchemp = {"UserInfoSearchCond": {
                "searchID": "3",
                "searchResultPosition": 0,
                "maxResults": 200,
                "EmployeeNoList":[]
            }
        }
        res = self.request(
            method="POST",
            path="/ISAPI/AccessControl/UserInfo/Search?format=json",
            json=searchemp,
        )
        return res
    
    def event_search(self):
        print ('Event search...')
        eventsearch = {"AcsEventCond": {
            "searchID":"1",
            "searchResultPosition":0,
            "maxResults":100,
            "major":0,
            "minor":0,
            "startTime": "2025-08-15T00:00:00+08:00",
            "endTime": "2025-08-15T23:59:59+08:00",
            }
        }
        res = self.request(
            method="POST",
            path="/ISAPI/AccessControl/AcsEvent?format=json",
            json=eventsearch,
        )
        return res
    
    
    def OLD_all_event_search(self,dataInicio=None,dataFim=None):
        print ('All Event search...')
        # Get today's date in YYYY-MM-DD format
        today = datetime.now().strftime("%Y-%m-%d")

        if dataInicio and dataFim:
            #set dates
            eventsearch = {"AcsEventCond": {
                "searchID":"1",
                "searchResultPosition":0,
                "maxResults":100,
                "major":0,
                "minor":0,
                "startTime": dataInicio + "T00:00:00+05:00",
                "endTime": dataFim + "T23:59:59+08:00",
                }
            }

        else:
            eventsearch = {"AcsEventCond": {
                "searchID":"2",
                "searchResultPosition":25,  #TODO from 1 to 25 until we find out how to get all at once
                "maxResults":100,
                "major":0,
                "minor":0,
                "startTime": str(today) + "T00:00:00+05:00",
                "endTime": str(today) + "T23:59:59+08:00",
                }
            }
        res = self.request(
            method="POST",
            path="/ISAPI/AccessControl/AcsEvent?format=json",
            json=eventsearch,
        )
        return res    
    
    def all_event_search_V0(self,dataInicio=None,dataFim=None):
        print ('All Event search...')
        # Get today's date in YYYY-MM-DD format
        today = datetime.now().strftime("%Y-%m-%d")
        '''
        if dataInicio and dataFim:
            #set dates
            eventsearch = {"AcsEventCond": {
                "searchID":"1",
                "searchResultPosition":0,
                "maxResults":100,
                "major":0,
                "minor":0,
                "startTime": dataInicio + "T00:00:00+05:00",
                "endTime": dataFim + "T23:59:59+08:00",
                }
            }

        else:
            eventsearch = {"AcsEventCond": {
                "searchID":"2",
                "searchResultPosition":25,  #TODO from 1 to 25 until we find out how to get all at once
                "maxResults":100,
                "major":0,
                "minor":0,
                "startTime": str(today) + "T00:00:00+05:00",
                "endTime": str(today) + "T23:59:59+08:00",
                }
            }
        res = self.request(
            method="POST",
            path="/ISAPI/AccessControl/AcsEvent?format=json",
            json=eventsearch,
        )
        return res    
        '''
    

        # Loop through searchResultPosition from 0 to 25
        all_events = []

        for search_result_position in range(0, 26):

            if dataInicio and dataFim:
                #set dates
                eventsearch = {"AcsEventCond": {
                    "searchID":"1",
                    "searchResultPosition":search_result_position,
                    "maxResults":100,
                    "major":0,
                    "minor":0,
                    "startTime": dataInicio + "T00:00:00+05:00",
                    "endTime": dataFim + "T23:59:59+08:00",
                    }
                }

            else:

                eventsearch = {
                    "AcsEventCond": {
                        "searchID": "2",
                        "searchResultPosition": search_result_position,
                        "maxResults": 100,
                        "major": 0,
                        "minor": 0,
                        "startTime": str(today) + "T00:00:00+05:00",
                        "endTime": str(today) + "T23:59:59+08:00",
                    }
                }
            
            res = self.request(
                method="POST",
                path="/ISAPI/AccessControl/AcsEvent?format=json",
                json=eventsearch,
            )
            print ('resssssss')
            print ('tem attr ', hasattr(res, 'json'))
            print ('callable ', callable(getattr(res, 'json')))
            print (res.json())
            
            # Optional: Add a small delay to avoid overwhelming the API
            # time.sleep(0.1)

            # Assuming res contains JSON data with events
            # Extract the events and add them to your list
            if hasattr(res, 'json') and callable(getattr(res, 'json')):
                events_data = res.json()
                # Adjust this based on the actual structure of your response
                if 'AcsEvent' in events_data:
                    #all_events.extend(events_data['AcsEvent'])
                    all_events.append(events_data)
            else:
                # If res is already the parsed data
                print ('aqqqqqui')
                return
                if isinstance(res, dict) and 'AcsEvent' in res:
                    all_events.extend(res)

        # Now all_events contains all events from positions 0 through 25
        print ('========================')
        print (all_events)
        print ('////////////////////////')
        print (all_events[0])
        print ('//////////////////////////')
        print (all_events[1])
        print ('================')
        print (len(all_events))
        print (all_events[0]['AcsEvent'])

        return

        return all_events

    def all_event_search(self,dataInicio=None,dataFim=None):
        print ('All Event search...')
        # Get today's date in YYYY-MM-DD format
        today = datetime.now().strftime("%Y-%m-%d")

        #FIX 08-09-2025
        diaHoje = datetime.today().day

        if diaHoje == 8 or diaHoje == 25 or diaHoje == 31 or diaHoje == 28 or diaHoje == 30:
            #Get data from day 1
            # Get the first response to use as base structure
            base_eventsearch = {
                "AcsEventCond": {
                    "searchID": "2",
                    "searchResultPosition": 0,
                    "maxResults": 100,
                    "major": 0,
                    "minor": 0,
                    "startTime": str(get_first_day(today)) + "T00:00:00+05:00",
                    "endTime": str(get_last_day(today)) + "T23:59:59+08:00",
                }
            }

        else:            
            # Get the first response to use as base structure
            base_eventsearch = {
                "AcsEventCond": {
                    "searchID": "2",
                    "searchResultPosition": 0,
                    "maxResults": 100,
                    "major": 0,
                    "minor": 0,
                    "startTime": str(today) + "T00:00:00+05:00",
                    "endTime": str(today) + "T23:59:59+08:00",
                }
            }

        base_res = self.request(
            method="POST",
            path="/ISAPI/AccessControl/AcsEvent?format=json",
            json=base_eventsearch,
        )

        # Parse base response
        if hasattr(base_res, 'json') and callable(getattr(base_res, 'json')):
            merged_result = base_res.json()
        else:
            merged_result = base_res

        # Collect all events from subsequent positions
        all_events = []

        # Add events from position 0 (already in merged_result)
        if isinstance(merged_result, dict):
            if 'AcsEvent' in merged_result:
                all_events.extend(merged_result['AcsEvent']['InfoList'])
            elif 'events' in merged_result:
                all_events.extend(merged_result['events'])

        if diaHoje == 8 or diaHoje == 25 or diaHoje == 31 or diaHoje == 28 or diaHoje == 30:
            # Loop through positions 1 to 25
            #for search_result_position in range(1, 26):
            tmpdia = 1
            diaTeste = get_first_day(today) #expected result 2025-08-01
            while tmpdia <= diaHoje:

                for search_result_position in range(10, 101, 10):
                    eventsearch = {
                        "AcsEventCond": {
                            "searchID": "2",
                            "searchResultPosition": search_result_position,
                            "maxResults": 100,
                            "major": 0,
                            "minor": 0,
                            "startTime": str(diaTeste) + "T00:00:00+05:00",
                            "endTime": str(diaTeste) + "T23:59:59+08:00",
                        }
                    }
                    
                    res = self.request(
                        method="POST",
                        path="/ISAPI/AccessControl/AcsEvent?format=json",
                        json=eventsearch,
                    )
                    
                    # Extract events from response
                    if hasattr(res, 'json') and callable(getattr(res, 'json')):
                        response_data = res.json()
                    else:
                        response_data = res
                    
                    if isinstance(response_data, dict):
                        if 'AcsEvent' in response_data:
                            print ('TEM ACSEVENT... MAS TEM INFILIST!!!!')
                            print (response_data['AcsEvent'])
                            print ('TEM OU NOA ', 'InfoList' in response_data['AcsEvent'])
                            if "InfoList" in response_data['AcsEvent']:
                                all_events.extend(response_data['AcsEvent']['InfoList'])
                        elif 'events' in response_data:
                            all_events.extend(response_data['events'])

                    # Optional: Add a small delay to avoid overwhelming the API
                    time.sleep(0.2)

                tmpdia += 1
                # Convert string to datetime object
                date_obj = datetime.strptime(diaTeste, '%Y-%m-%d')

                # Add one day using timedelta
                new_date = date_obj + timedelta(days=1)

                # Convert back to string if needed
                diaTeste = new_date.strftime('%Y-%m-%d')

        else:            
            # Loop through positions 1 to 25
            #for search_result_position in range(1, 26):
            for search_result_position in range(10, 101, 10):
                eventsearch = {
                    "AcsEventCond": {
                        "searchID": "2",
                        "searchResultPosition": search_result_position,
                        "maxResults": 100,
                        "major": 0,
                        "minor": 0,
                        "startTime": str(today) + "T00:00:00+05:00",
                        "endTime": str(today) + "T23:59:59+08:00",
                    }
                }
                
                res = self.request(
                    method="POST",
                    path="/ISAPI/AccessControl/AcsEvent?format=json",
                    json=eventsearch,
                )
                
                # Extract events from response
                if hasattr(res, 'json') and callable(getattr(res, 'json')):
                    response_data = res.json()
                else:
                    response_data = res
                
                if isinstance(response_data, dict):
                    if 'AcsEvent' in response_data:
                        print ('TEM ACSEVENT... MAS TEM INFILIST!!!!')
                        print (response_data['AcsEvent'])
                        print ('TEM OU NOA ', 'InfoList' in response_data['AcsEvent'])
                        if "InfoList" in response_data['AcsEvent']:
                            all_events.extend(response_data['AcsEvent']['InfoList'])
                    elif 'events' in response_data:
                        all_events.extend(response_data['events'])

                # Optional: Add a small delay to avoid overwhelming the API
                time.sleep(0.2)

        # Update the merged result with all collected events
        if 'AcsEvent' in merged_result:
            merged_result['AcsEvent']['InfoList'] = all_events
        elif 'events' in merged_result:
            merged_result['events'] = all_events
        else:
            # If the structure is different, add events as a new key
            merged_result['allEvents'] = all_events

        # Now merged_result contains a single record with all events     
        # 

        return merged_result   
    


def get_first_day(dt, d_years=0, d_months=0):
	# d_years, d_months are "deltas" to apply to dt
	y, m = dt.year + d_years, dt.month + d_months
	a, m = divmod(m-1, 12)
	return date(y+a, m+1, 1)

def get_last_day(dt):
	return get_first_day(dt, 0, 1) + timedelta(-1)