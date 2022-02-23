import datetime
import logging
import requests
import json
import urllib3
from time import gmtime, strftime, sleep, time

# test cases: get all kpi's, all alerts, accounts list

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG,  # If smth wrong, change to 'DEBUG'
                    filename="dashboard.log")  # Name of log file
logger = logging.getLogger("Netformx")
login_email = "mrbean01@netformx.com"
password = "Netformx4"
timeout = 15  # Timeout for APIs check (login not included!), in seconds
loop_time = 60  # Time between every loop, in seconds


def main_dashboard_screen():
    with requests.Session() as s:
        s.post('https://login.netformx.com/licensing/api/login/cisco/',  # Auth, get cookies
               json={"CiscoUserNameOrCiscoEmail": login_email,
                     "CiscoPassword": password,
                     "AppReturnUrl": "https://successxpert.netformx.com/dashboard"})

        # Get all kpi's
        url = 'https://successxpert.netformx.com/healthscore/api/v1/dashboard/header-kpis'
        api_kpis_response = s.get(url)
        if api_kpis_response.status_code == 200:
            logger.info(api_kpis_response.text)
        else:
            logger.error("Failed!")

        # Get all alerts
        url = 'https://successxpert.netformx.com/alerts/api/v1/logs/get-alerts'
        data = {"Accounts": [], "Types": [], "FromDate": str(datetime.datetime.now())}
        api_alerts_response = s.post(url, json=data)
        if api_alerts_response.status_code == 200:
            logger.info(api_alerts_response.text)
        else:
            logger.error("Failed!")

        # Get accounts list
        url = 'https://successxpert.netformx.com/healthscore/api/v1/dashboard/accounts-list'
        api_accounts_response = s.get(url)
        account_data = json.loads(api_accounts_response.text)
        if api_accounts_response.status_code == 200:
            logger.info(api_accounts_response.text)
        else:
            logger.error("Failed!")


main_dashboard_screen()
