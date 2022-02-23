import json
import logging

import requests

# test cases: get all tenant accounts,
# test cases: get header kpi's, health score, interactions, alerts by account
# test cases: recalculate by account

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG,  # If smth wrong, change to 'DEBUG'
                    filename="accounts_screen.log")  # Name of log file
logger = logging.getLogger("Netformx")
login_email = "mrbean01@netformx.com"
password = "Netformx4"
timeout = 15  # Timeout for APIs check (login not included!), in seconds
loop_time = 60  # Time between every loop, in seconds


def main_accounts():
    with requests.Session() as s:
        s.post('https://login.netformx.com/licensing/api/login/cisco/',  # Auth, get cookies
               json={"CiscoUserNameOrCiscoEmail": login_email,
                     "CiscoPassword": password,
                     "AppReturnUrl": "https://successxpert.netformx.com/dashboard"})

        # GET requests
        # get all tenant accounts
        url = 'https://successxpert.netformx.com/accounts/api/v1/accounts/get-tenant-accounts?includeEndCustomerNames' \
              '=true '
        api_accounts_response = s.get(url)
        accounts_data = json.loads(api_accounts_response.text)
        if api_accounts_response.status_code == 200:
            logger.info(api_accounts_response.text)
        else:
            logger.error(api_accounts_response.status_code, "Failed!")

        # get header kpis by account
        for item in accounts_data:
            url = 'https://successxpert.netformx.com/healthscore/api/v1/healthscore/header-kpis/' + item['id']
            api_kpis_response = s.get(url)
            logger.info(api_kpis_response.text)

        # get health score by account
        for item in accounts_data:
            url = 'https://successxpert.netformx.com/healthscore/api/v1/healthscore/' + item['id']
            api_healthscore_response = s.get(url)
            logger.info(api_healthscore_response.text)

        # get interactions by account
        for item in accounts_data:
            data = {'accountid=': item['id']}
            url = 'https://successxpert.netformx.com/interactions/api/v1/interactions/get-by-account-id'
            api_interactions_response = s.get(url, json=data)
            logger.info(api_interactions_response.text)

        # get about info by account
        for item in accounts_data:
            url = 'https://successxpert.netformx.com/accounts/api/v1/accounts/' + item['id']
            api_about_response = s.get(url)
            logger.info(api_about_response.text)

        # POST requests
        # recalculate health score for all accounts
        for item in accounts_data:
            url = 'https://successxpert.netformx.com/healthscore/api/v1/healthscore/calculation'
            data = {"tenantId": 1, "accountId": item['id']}
            recalculate_response = s.post(url, json=data)
            if recalculate_response.status_code == 200:
                logger.info("Succeeded!")
            else:
                logger.info(recalculate_response.status_code)

        # get alerts for specific account
        for item in accounts_data:
            payload = {"Accounts": item['id'], "Types": [], "Count": 5}
            url = 'https://successxpert.netformx.com/alerts/api/v1/logs/get-alerts'  # 400 {"errors":{"Accounts":[
            # "Error converting value \account_id\" to type 'System.Collections.Generic.IEnumerable`1[System.String]'
            api_alerts_response = s.post(url, params=payload)
            logger.info(api_alerts_response.text)


main_accounts()
