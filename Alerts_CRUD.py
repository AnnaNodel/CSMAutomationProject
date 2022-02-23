import logging
import requests
import json
import datetime
import urllib3
from time import gmtime, strftime, sleep, time

# test cases: create new alert rule, create alert from a rule, edit rule, delete rule

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG,  # If smth wrong, change to 'DEBUG'
                    filename="alerts_crud.log")  # Name of log file
logger = logging.getLogger("Netformx")
login_email = "mrbean01@netformx.com"
password = "Netformx4"
timeout = 15  # Timeout for APIs check (login not included!), in seconds
loop_time = 60  # Time between every loop, in seconds


def main_create_rule():
    with requests.Session() as s:
        s.post('https://login.netformx.com/licensing/api/login/cisco/',  # Auth, get cookies
               json={"CiscoUserNameOrCiscoEmail": login_email,
                     "CiscoPassword": password,
                     "AppReturnUrl": "https://successxpert.netformx.com/dashboard"})

        # create rule
        data = {"type": 5, "accounts": ["ec83292b-b3b3-4a97-af90-b62dee1d409b"],
                "name": "Automated Pipeline Close Rate rule - Dacia",
                "description": "Automated Pipeline Close Rate rule - Dacia", "playBookId": "", "scoreCategory": 1,
                "period": 1, "duration": 1, "severity": 0, "emailRecipients": "", "isActive": True}

        api_response_rules = s.post("https://successxpert.netformx.com/alerts/api/v1/rules",
                                    json=data)

        returned_data_rules = json.loads(api_response_rules.text)
        if api_response_rules.status_code in (200, 201, 202, 203, 204):
            logger.info("Rule is created")
            logger.info(returned_data_rules)
            created_rule_id = returned_data_rules['id']  # save rule id for next actions
        else:
            logger.error(api_response_rules.status_code, "Rule is failed")

        # run created rule
        url = 'https://successxpert.netformx.com/alerts/api/v1/rules/run'
        params = {'id': created_rule_id}
        run_response = s.post(url, params=params)
        if run_response.status_code in (200, 201, 202, 203, 204):
            logger.info("Alert is added from a rule")
        else:
            logger.error(run_response.status_code, "Alert is not run!")

        # edit rule
        updated_data = {"type": 5, "name": "Rule for automation tests - updated",
                        "description": "Automated Pipeline Close Rate rule - Dacia - Updated",
                        "accounts": ["ec83292b-b3b3-4a97-af90-b62dee1d409b"], "playBookId": "", "scoreCategory": 1,
                        "period": 1, "duration": 1, "severity": 1, "emailRecipients": "", "tenantId": 1,
                        "createdBy": "mrbean01@netformx.com", "isActive": True, "id": created_rule_id,
                        "modifyDate": str(datetime.datetime.now()), "createdDate": str(datetime.datetime.now()),
                        "accountNames": ["Dacia"]}

        url = 'https://successxpert.netformx.com/alerts/api/v1/rules'
        update_response = s.put(url, json=updated_data)
        if update_response.status_code == 200:
            logger.info("Rule updated")
        else:
            logger.error(update_response.status_code, "Failed!")

        # delete created rule
        url = 'https://successxpert.netformx.com/alerts/api/v1/rules/' + created_rule_id
        delete_response = s.delete(url)
        if delete_response.status_code in (200, 201, 202, 204):
            logger.info("Created rule is deleted")
        elif delete_response.status_code == 404:
            logger.debug("Rule is not found")
        else:
            logger.error(delete_response.status_code, "Failed")


main_create_rule()
