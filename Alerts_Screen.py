import logging
import requests
import json
import datetime
import urllib3
from time import gmtime, strftime, sleep, time

# test cases: Get all alert rules, # Get alert rules by type

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG,  # If smth wrong, change to 'DEBUG'
                    filename="alerts_screen.log")  # Name of log file
logger = logging.getLogger("Netformx")
login_email = "mrbean01@netformx.com"
password = "Netformx4"
timeout = 15  # Timeout for APIs check (login not included!), in seconds
loop_time = 60  # Time between every loop, in seconds


def main_alerts():
    with requests.Session() as s:
        s.post('https://login.netformx.com/licensing/api/login/cisco/',  # Auth, get cookies
               json={"CiscoUserNameOrCiscoEmail": login_email,
                     "CiscoPassword": password,
                     "AppReturnUrl": "https://successxpert.netformx.com/dashboard"})

        # Get all tenant accounts
        url = 'https://successxpert.netformx.com/accounts/api/v1/accounts/get-tenant-accounts?includeEndCustomerNames' \
              '=true '
        api_accounts_response = s.get(url)
        accounts_data = json.loads(api_accounts_response.text)
        if api_accounts_response.status_code == 200:
            logger.info(api_accounts_response.text)
        else:
            logger.error(api_accounts_response.status_code, "Failed!")

        # Get all alert rules
        data = {"Accounts": [], "Types": []}
        url = 'https://successxpert.netformx.com/alerts/api/v1/rules/get-rules'
        api_rules_response = s.post(url, json=data)
        if api_rules_response.status_code == 200:
            logger.info(api_rules_response.text)
        else:
            logger.info(api_rules_response.status_code)

        # Get alert rules by account

        # Get alerts by account

        # Get alert rules by type
        type_numbers = [0, 1, 2, 3, 4, 5, 6, 7]
        for item in type_numbers:
            data = {"Accounts": [], "Types": [item]}
            url = 'https://successxpert.netformx.com/alerts/api/v1/rules/get-rules'
            api_types_response = s.post(url, json=data)
            if api_types_response.status_code == 200:
                logger.info(api_types_response.text)
            else:
                logger.warning(api_types_response.status_code)


main_alerts()
