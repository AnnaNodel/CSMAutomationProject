import datetime
import json
import logging
from time import gmtime, strftime
from requests.auth import HTTPBasicAuth
import requests

# test cases: get health score configuration screen by account, edit health score configuration for specific account

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG,  # If smth wrong, change to 'DEBUG'
                    filename="configuration_healthScore.log")  # Name of log file
logger = logging.getLogger("Netformx")
login_email = "mrbean01@netformx.com"
password = "Netformx4"
timeout = 15  # Timeout for APIs check (login not included!), in seconds
loop_time = 60  # Time between every loop, in seconds


def main_configuration_health_score():
    with requests.Session() as s:
        s.post('https://login.netformx.com/licensing/api/login/cisco/',  # Auth, get cookies
               json={"CiscoUserNameOrCiscoEmail": login_email,
                     "CiscoPassword": password,
                     "AppReturnUrl": "https://successxpert.netformx.com/dashboard"})

        # get all tenant accounts
        url = 'https://successxpert.netformx.com/accounts/api/v1/accounts/get-tenant-accounts?includeEndCustomerNames' \
              '=true '
        api_accounts_response = s.get(url)
        accounts_data = json.loads(api_accounts_response.text)
        logger.info(api_accounts_response.status_code)

        # get health score configuration screen by account
        for item in accounts_data:
            url = 'https://successxpert.netformx.com/healthscore/api/v1/healthscore/configuration/' + item['id']
            api_healthScore_configuration_response = s.get(url)
            logger.info(api_healthScore_configuration_response.text)

        # edit health score configuration for specific account
        for item in accounts_data:
            data = {"id": "6190f334d019a64f7a348f60", "accountId": item['id'], "tenantId": 1, "utilization": 35,
                    "support": 15, "financial": 30, "sentiment": 20}
            url = 'https://successxpert.netformx.com/healthscore/api/v1/healthscore/relative-weight'
            api_edit_configuration_response = s.post(url, json=data)
            logger.info(item['name'])
            logger.info(api_edit_configuration_response.status_code)


main_configuration_health_score()
