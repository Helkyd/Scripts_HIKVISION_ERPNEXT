import logging
import os
from typing import Literal

import requests
from requests.auth import HTTPDigestAuth
from requests.exceptions import HTTPError


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
            "startTime": "2025-08-15T06:00:00+08:00",
            "endTime": "2025-08-15T22:00:00+08:00",
            }
        }
        res = self.request(
            method="POST",
            path="/ISAPI/AccessControl/AcsEvent?format=json",
            json=eventsearch,
        )
        return res