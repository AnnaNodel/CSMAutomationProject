import datetime
import json
import logging
from time import gmtime, strftime
from requests.auth import HTTPBasicAuth
import requests

# test cases: get all interaction, get interactions by type, get interactions by account

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG,  # If smth wrong, change to 'DEBUG'
                    filename="interactions_screen.log")  # Name of log file
logger = logging.getLogger("Netformx")
login_email = "mrbean01@netformx.com"
password = "Netformx4"
timeout = 15  # Timeout for APIs check (login not included!), in seconds
loop_time = 60  # Time between every loop, in seconds


def main_interactions():
    with requests.Session() as s:
        s.post('https://login.netformx.com/licensing/api/login/cisco/',  # Auth, get cookies
               json={"CiscoUserNameOrCiscoEmail": login_email,
                     "CiscoPassword": password,
                     "AppReturnUrl": "https://successxpert.netformx.com/dashboard"})

        # Get all interactions
        url = 'https://successxpert.netformx.com/interactions/api/v1/interactions?isCompleted=false'
        api_interactions_response = s.get(url)
        interaction_data = json.loads(api_interactions_response.text)
        if api_interactions_response.status_code == 200:
            logger.info(api_interactions_response.text)
        else:
            logger.error(api_interactions_response.status_code, "Failed!")

        # Get interactions by type
        interaction_type = [1, 2, 3, 4]
        for item in interaction_type:
            payload = {'interactionType': item, 'isCompleted': False}
            url = 'https://successxpert.netformx.com/interactions/api/v1/interactions/'
            api_playbook_response = s.get(url, params=payload)
            if api_playbook_response.status_code == 200:
                logger.info(api_playbook_response.text)
            else:
                logger.debug(api_playbook_response.status_code, "Failed!")

        # Get interactions by account
        url = 'https://successxpert.netformx.com/accounts/api/v1/accounts/get-tenant-accounts?includeEndCustomerNames' \
              '=true '
        api_accounts_response = s.get(url)
        accounts_data = json.loads(api_accounts_response.text)
        for item in accounts_data:
            payload = {'AccountId': item['id'], 'isCompleted': False}
            url = 'https://successxpert.netformx.com/interactions/api/v1/interactions'
            api_results_response = s.get(url, params=payload)
            if api_results_response.status_code == 200:
                logger.info(api_results_response.text)
            else:
                logger.debug(api_results_response.status_code)


main_interactions()
