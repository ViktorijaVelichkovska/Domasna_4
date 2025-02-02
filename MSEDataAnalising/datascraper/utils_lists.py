import os
import django
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from bs4 import BeautifulSoup
import requests
import time
from datetime import datetime, timedelta
from selenium.webdriver.chrome.options import Options
import pandas as pd

def init_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-webgl")
    chrome_options.add_argument("--disable-blink-features=CSSStyling")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")

    prefs = {
        "profile.managed_default_content_settings.images": 2,  # Disable images
        "profile.managed_default_content_settings.javascript": 2,  # Disable JavaScript
        "profile.default_content_setting_values.popups": 2,  # Block pop-ups
        "profile.default_content_setting_values.geolocation": 2,  # Disable geolocation
        "profile.default_content_setting_values.notifications": 2,  # Disable notifications
        "profile.password_manager_enabled": False,  # Disable password manager
        "credentials_enable_service": False,  # Disable credentials service
        "profile.content_settings.plugin_whitelist.adobe-flash-player": 0,  # Disable Flash
        "profile.content_settings.exceptions.plugins.*,*.per_resource.adobe-flash-player": 0
    }

    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=chrome_options)
    return driver


def get_10_year_data_list(company_code):
    data = []
    print("Thread started...")
    driver = init_driver()

    base_url = "https://www.mse.mk/mk/stats/symbolhistory/"
    url = base_url + company_code
    driver.get(url)

    years = 10
    end_date = datetime.now()
    start_date = end_date - timedelta(days=364)
    for i in range(years):
        data.extend(search_company_year_list(driver, company_code, end_date.strftime('%d.%m.%Y'),
                                             start_date.strftime('%d.%m.%Y')))
        end_date = start_date - timedelta(days=1)
        start_date = end_date - timedelta(days=365)

    driver.quit()
    print("Thread finnished...")

    return data


def get_data_from_day_list(company, date_from):
    date = []
    date_from = datetime.strptime(date_from, '%d.%m.%Y').date()
    driver = webdriver.Chrome()
    base_url = "https://www.mse.mk/mk/stats/symbolhistory/"
    url = base_url + company.company_code
    # driver.get(url)

    date_to = driver.find_element(By.ID, "ToDate")
    date_from = driver.find_element(By.ID, "FromDate")
    btn = driver.find_element(By.CLASS_NAME, "btn-primary-sm")

    new_data_to = datetime.now()
    new_data_from = date_from

    # BEAUTIFUL SOUP
    response = requests.get(url)
    raw_html = response.text
    soup = BeautifulSoup(raw_html, "html.parser")
    table = soup.find('table', id='resultsTable')

    driver.execute_script("arguments[0].value = arguments[1];", date_to, new_data_to)
    driver.execute_script("arguments[0].value = arguments[1];", date_from, new_data_from)
    btn.click()
    sleep(0.01)

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find('table', id='resultsTable')

    rows = None
    if table is not None:
        rows = table.find_all('tr')
    entries = []
    if rows is not None and len(rows) > 0:
        for row in rows:
            columns = row.find_all('td')
            if columns:
                columns_dict = {
                    "date": columns[0].text.strip(),
                    "last_transaction_price": columns[1].text.strip(),
                    "max_price": columns[2].text.strip(),
                    "min_price": columns[3].text.strip(),
                    "avg_price": columns[4].text.strip(),
                    "percentage": columns[5].text.strip(),
                    "profit": columns[6].text.strip(),
                    "total_profit": columns[7].text.strip(),
                    "company_code": company.company_code
                }
                date.append(columns_dict)

    return date


def search_company_year_list(driver, company_code, to_date, from_date):
    data = []
    base_url = "https://www.mse.mk/mk/stats/symbolhistory/"
    url = base_url + company_code
    # driver.get(url)

    date_to = driver.find_element(By.ID, "ToDate")
    date_from = driver.find_element(By.ID, "FromDate")
    btn = driver.find_element(By.CLASS_NAME, "btn-primary-sm")

    new_data_to = to_date
    new_data_from = from_date

    # BEAUTIFUL SOUP
    response = requests.get(url)
    raw_html = response.text
    soup = BeautifulSoup(raw_html, "html.parser")
    table = soup.find('table', id='resultsTable')

    driver.execute_script("arguments[0].value = arguments[1];", date_to, new_data_to)
    driver.execute_script("arguments[0].value = arguments[1];", date_from, new_data_from)
    btn.click()
    sleep(0.01)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find('table', id='resultsTable')

    rows = None
    if table is not None:
        rows = table.find_all('tr')

    if rows is not None and len(rows) > 0:
        for row in rows:
            columns = row.find_all('td')
            if columns:
                columns_dict = {
                    "date": columns[0].text.strip(),
                    "last_transaction_price": columns[1].text.strip(),
                    "max_price": columns[2].text.strip(),
                    "min_price": columns[3].text.strip(),
                    "avg_price": columns[4].text.strip(),
                    "percentage": columns[5].text.strip(),
                    "profit": columns[6].text.strip(),
                    "total_profit": columns[7].text.strip(),
                    "company_code": company_code
                }
                data.append(columns_dict)
    return data


if __name__ == "__main__":
    start_time = time.time()
    data = get_10_year_data_list("KMB")
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Total execution time: {execution_time:.2f} seconds")
    df = pd.DataFrame(data)
    df.to_csv("data.csv")
    print(data)