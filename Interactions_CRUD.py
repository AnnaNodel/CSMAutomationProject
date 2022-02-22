import datetime
import json
import logging
from time import gmtime, strftime
from requests.auth import HTTPBasicAuth
import requests

# test cases: get all interactions, get interactions of specific account
# test cases: create new interaction, edit created interaction, delete created interaction
# test cases: create overdue interaction, edit overdue interaction, delete created overdue interaction

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG,  # If smth wrong, change to 'DEBUG'
                    filename="interactions_crud.log")  # Name of log file
logger = logging.getLogger("Netformx")
login_email = "mrbean01@netformx.com"
password = "Netformx4"
timeout = 15  # Timeout for APIs check (login not included!), in seconds
loop_time = 60  # Time between every loop, in seconds


def main_create_interaction():
    with requests.Session() as s:
        s.post('https://login.netformx.com/licensing/api/login/cisco/',  # Auth, get cookies
               json={"CiscoUserNameOrCiscoEmail": login_email,
                     "CiscoPassword": password,
                     "AppReturnUrl": "https://successxpert.netformx.com/dashboard"})

    # create new interaction
    data = {"name": "Automated Call Interaction - Dacia", "accountId": "ec83292b-b3b3-4a97-af90-b62dee1d409b",
            "type": 2,
            "description": "Automated Call Interaction - Dacia",
            "dueDate": str(datetime.datetime.now() + datetime.timedelta(days=1)),
            "emailRecipients": "", "daysBefore": 0, "creationDate": str(datetime.datetime.now()),
            "isCompleted": False, "notifyBeforeDueDate": True, "modifyDate": str(datetime.datetime.now()), "steps": [],
            "timeOffset": -120}

    api_response_create = s.post("https://successxpert.netformx.com/interactions/api/v1/interactions/create",
                                 json=data)

    returned_data_create = json.loads(api_response_create.text)
    if api_response_create.status_code in (200, 201, 202, 203, 204):
        logger.info("Interaction is created")
        logger.info(returned_data_create)
        created_interaction_id = returned_data_create['id']  # save interaction id for next actions
    else:
        logger.error(api_response_create.status_code, "Interaction is failed!")

    # edit created interaction
    updated_data = {"id": created_interaction_id, "name": "Call interaction for automation tests - Updated",
                    "accountId": "ec83292b-b3b3-4a97-af90-b62dee1d409b", "tenantId": 1,
                    "description": "Call interaction for automation tests - Updated",
                    "createdBy": "mrbean01@netformx.com",
                    "modifiedBy": "mrbean01@netformx.com", "modifyDate": str(datetime.datetime.now()),
                    "creationDate": str(datetime.datetime.now()),
                    "dueDate": str(datetime.datetime.now() + datetime.timedelta(days=1)), "daysBefore": 0,
                    "notifyBeforeDueDate": True, "isCompleted": False, "type": 2, "steps": [], "emailRecipients": "",
                    "playbookId": "", "ruleId": "", "notes": "", "playbookFilePath": "", "timeOffset": -120,
                    "notificationSent": False, "completedSteps": 0, "iconClass": "csm-icon-call",
                    "accountName": "Dacia"}

    url = 'https://successxpert.netformx.com/interactions/api/v1/interactions/' + created_interaction_id
    api_response_update = s.put(url, json=updated_data)
    if api_response_update.status_code == 200:
        logger.info("Interaction updated")
    else:
        logger.error(api_response_update.status_code, "Failed!")

    # delete created interaction
    url = 'https://successxpert.netformx.com/interactions/api/v1/interactions/' + created_interaction_id
    delete_interaction_response = s.delete(url)
    if delete_interaction_response.status_code in (200, 201, 202, 204):
        logger.info("Interaction is deleted")
    elif delete_interaction_response.status_code == 404:
        logger.debug("Interaction is not found")
    else:
        logger.error(delete_interaction_response.status_code, "Failed")


main_create_interaction()


def main_create_overdue_interaction():
    with requests.Session() as s:
        s.post('https://login.netformx.com/licensing/api/login/cisco/',  # Auth, get cookies
               json={"CiscoUserNameOrCiscoEmail": login_email,
                     "CiscoPassword": password,
                     "AppReturnUrl": "https://successxpert.netformx.com/dashboard"})

    # create new overdue interaction
    data = {"name": "Automated Overdue Meeting Interaction - Dacia",
            "accountId": "ec83292b-b3b3-4a97-af90-b62dee1d409b", "type": 3,
            "description": "Automated Overdue Meeting Interaction - Dacia",
            "dueDate": str(datetime.datetime.now() - datetime.timedelta(days=1)),
            "emailRecipients": "",
            "daysBefore": 0, "creationDate": str(datetime.datetime.now() - datetime.timedelta(days=1)),
            "isCompleted": False,
            "notifyBeforeDueDate": True, "modifyDate": str(datetime.datetime.now() - datetime.timedelta(days=1)),
            "steps": [], "timeOffset": -120}

    api_response_create_overdue = s.post("https://successxpert.netformx.com/interactions/api/v1/interactions/create",
                                         json=data)

    returned_data_create_overdue = json.loads(api_response_create_overdue.text)
    if api_response_create_overdue.status_code == 200:
        logger.info("Overdue Interaction is created")
        logger.info(returned_data_create_overdue)
        overdue_interaction_id = returned_data_create_overdue['id']  # save interaction id for next actions
    else:
        logger.error(api_response_create_overdue.status_code, "Overdue interaction is failed!")

    # edit overdue interaction
    updated_data = {"id": overdue_interaction_id, "name": "Call interaction for automation tests - Updated",
                    "accountId": "ec83292b-b3b3-4a97-af90-b62dee1d409b", "tenantId": 1,
                    "description": "Call interaction for automation tests - Updated",
                    "createdBy": "mrbean01@netformx.com",
                    "modifiedBy": "mrbean01@netformx.com",
                    "modifyDate": str(datetime.datetime.now() - datetime.timedelta(days=1)),
                    "creationDate": str(datetime.datetime.now() - datetime.timedelta(days=1)),
                    "dueDate": str(datetime.datetime.now() - datetime.timedelta(days=2)), "daysBefore": 0,
                    "notifyBeforeDueDate": True, "isCompleted": False, "type": 2, "steps": [],
                    "emailRecipients": "",
                    "playbookId": "", "ruleId": "", "notes": "", "playbookFilePath": "", "timeOffset": -120,
                    "notificationSent": False, "completedSteps": 0, "iconClass": "csm-icon-call",
                    "accountName": "Dacia"}

    url = 'https://successxpert.netformx.com/interactions/api/v1/interactions/' + overdue_interaction_id
    api_response_update = s.put(url, json=updated_data)
    if api_response_update.status_code == 200:
        logger.info("Overdue Interaction updated")
    else:
        logger.error(api_response_update.status_code, "Failed!")

    # delete overdue interaction
    url = 'https://successxpert.netformx.com/interactions/api/v1/interactions/' + overdue_interaction_id
    delete_overdue_response = s.delete(url)
    if delete_overdue_response.status_code in (200, 201, 202, 204):
        logger.info("Overdue Interaction is deleted")
    elif delete_overdue_response.status_code == 404:
        logger.debug("Interaction is not found")
    else:
        logger.error(delete_overdue_response.status_code, "Failed")


main_create_overdue_interaction()
