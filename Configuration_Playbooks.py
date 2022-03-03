import datetime
import json
import logging
from time import gmtime, strftime
from requests.auth import HTTPBasicAuth
import requests

# test cases: get all interaction, get interactions by type, get interactions by account

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG,  # If smth wrong, change to 'DEBUG'
                    filename="configuration_playbooks.log")  # Name of log file
logger = logging.getLogger("Netformx")
login_email = "mrbean01@netformx.com"
password = "Netformx4"
timeout = 15  # Timeout for APIs check (login not included!), in seconds
loop_time = 60  # Time between every loop, in seconds


def main_configuration_playbooks():
    with requests.Session() as s:
        s.post('https://login.netformx.com/licensing/api/login/cisco/',  # Auth, get cookies
               json={"CiscoUserNameOrCiscoEmail": login_email,
                     "CiscoPassword": password,
                     "AppReturnUrl": "https://successxpert.netformx.com/dashboard"})

        # get playbooks by created by
        data = {"CreatedByList": []}
        url = 'https://successxpert.netformx.com/playbooks/api/v1/playbooks/get-playbooks'
        api_createdby_response = s.post(url, json=data)
        if api_createdby_response.status_code == 200:
            logger.info(api_createdby_response.text)
        else:
            logger.warning(api_createdby_response.status_code)

        data = {"CreatedByList": ["System"]}
        url = 'https://successxpert.netformx.com/playbooks/api/v1/playbooks/get-playbooks'
        api_createdby_response = s.post(url, json=data)
        if api_createdby_response.status_code == 200:
            logger.info(api_createdby_response.text)
        else:
            logger.warning(api_createdby_response.status_code)

        data = {"CreatedByList": [login_email]}
        url = 'https://successxpert.netformx.com/playbooks/api/v1/playbooks/get-playbooks'
        api_createdby_response = s.post(url, json=data)
        if api_createdby_response.status_code == 200:
            logger.info(api_createdby_response.text)
        else:
            logger.warning(api_createdby_response.status_code)

        # create custom playbook
        url = 'https://successxpert.netformx.com/playbooks/api/v1/playbooks'
        data = {"name": "Automation test Playbook", "description": "Automation test Playbook",
                "actionItems": [{"name": "Create", "order": 0, "filePath": "", "dueDateInDays": 1},
                                {"name": "Read", "order": 1, "filePath": "", "dueDateInDays": 1},
                                {"name": "Update", "order": 2, "filePath": "", "dueDateInDays": 1},
                                {"name": "Delete", "order": 3, "filePath": "", "dueDateInDays": 1}],
                "filePath": 0, "dueDateInDays": 1}
        api_createPlaybook_response = s.post(url, json=data)
        returned_playbook_data = json.loads(api_createPlaybook_response.text)
        if api_createPlaybook_response.status_code in (200, 201, 202, 203, 204):
            logger.info("Playbook created")
            logger.info(returned_playbook_data)
            created_playbook_id = returned_playbook_data['id']
        else:
            logger.info(api_createPlaybook_response.status_code)

        """"# verify that created custom playbook is displayed
        url = 'https://successxpert.netformx.com/playbooks/api/v1/playbooks/get-playbooks'
        data = {"CreatedByList": []}
        api_search_response = s.post(url, json=data)
        created_playbook_search = json.loads(api_search_response.text)
        for item in created_playbook_search:
            if created_playbook_search['id'] == created_playbook_id:
                logger.info(created_playbook_id)
            else:
                pass"""

        # edit created custom playbook
        url = 'https://successxpert.netformx.com/playbooks/api/v1/playbooks'
        updated_data = {"id": created_playbook_id, "name": "Automation test Playbook",
                        "description": "Automation test Playbook", "dueDateInDays": 1,
                        "actionItems": [{"name": "Create", "order": 0, "filePath": "", "dueDateInDays": 2},
                                        {"name": "Read", "order": 1, "filePath": "", "dueDateInDays": 2},
                                        {"name": "Update", "order": 2, "filePath": "", "dueDateInDays": 2},
                                        {"name": "Delete", "order": 3, "filePath": "", "dueDateInDays": 2}],
                        "tenantId": 1, "createdBy": login_email, "createdDate": str(datetime.datetime.now()),
                        "filePath": 0}
        api_editPlaybook_response = s.put(url, json=updated_data)
        if api_editPlaybook_response.status_code == 200:
            logger.info("Playbook updated!")
        else:
            logger.info(api_editPlaybook_response.status_code)

        # delete created custom playbook
        url = 'https://successxpert.netformx.com/playbooks/api/v1/playbooks/' + created_playbook_id
        api_deletePlaybook_response = s.delete(url)
        if api_deletePlaybook_response.status_code in (200, 201, 202, 204):
            logger.info("Playbook deleted!")
        else:
            logger.info(api_deletePlaybook_response.status_code)


main_configuration_playbooks()
