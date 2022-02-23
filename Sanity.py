import requests
from time import gmtime, strftime, sleep, time
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG,  # If smth wrong, change to 'DEBUG'
                    filename="sanity.log")  # Name of log file
logger = logging.getLogger("Netformx")
login_email = "mrbean01@netformx.com"
password = "Netformx4"
timeout = 15  # Timeout for APIs check (login not included!), in seconds
loop_time = 60  # Time between every loop, in seconds


# If you need to print time of loops, in lines 46, 52, change 'debug' to 'info'

def main():
    with requests.Session() as s:
        s.post('https://login.netformx.com/licensing/api/login/cisco/',  # Auth, get cookies
               json={"CiscoUserNameOrCiscoEmail": login_email,
                     "CiscoPassword": password,
                     "AppReturnUrl": "https://successxpert.netformx.com/dashboard"})
        list_of_links_get = [
            "https://successxpert.netformx.com/accounts/api/v1/accounts/get-tenant-accounts",
            "https://successxpert.netformx.com/healthscore/api/v1/dashboard/accounts-list",
            "https://successxpert.netformx.com/healthscore/api/v1/dashboard/header-kpis",
            "https://customer-mappings.netformx.com/mapping"  # Mapping, optional
        ]

        list_of_links_post = [
            "https://successxpert.netformx.com/alerts/api/v1/rules/get-rules",
            "https://successxpert.netformx.com/alerts/api/v1/logs/get-alerts"
        ]

        for i in list_of_links_get:
            try:
                s.get(i, timeout=timeout)
            except requests.exceptions.ReadTimeout:
                logger.warning(("Timeout! GET method! ", i))

        for i in list_of_links_post:
            try:
                g = s.post(i, json={"Accounts": [], "Types": []}, timeout=timeout)
                print(g.text)
            except requests.exceptions.ReadTimeout:
                logger.warning(("Timeout! POST method! ", i))
        try:
            s.post("https://successxpert.netformx.com/alerts/api/v1/logs/get-alerts",
                   json={"Accounts": [], "Types": [], "FromDate": strftime('%Y-%m-%dT%X.000Z', gmtime())},
                   timeout=timeout)
        except requests.exceptions.ReadTimeout:
            logger.warning(("Timeout! POST method! ", i))


if __name__ == '__main__':
    logging.info(("Program started. Current timeout: " + str(timeout) + ", Loop time: " + str(loop_time)))
    while True:
        logger.debug("New lap of check")
        start_time = time()
        main()
        logger.debug(("Lap ended in: %.2f" % (time() - start_time) + " second"))
        sleep(loop_time)
