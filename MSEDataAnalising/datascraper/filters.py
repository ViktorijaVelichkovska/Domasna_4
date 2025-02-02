import os
from datetime import date
import requests
from bs4 import BeautifulSoup
from datascraper.utils import get_10_year_data, get_missing_data, save_company
from databaseTesting import get_last_date_string
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Process, Manager
import time


def worker(companies_subset, max_workers):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for company in companies_subset:
            executor.submit(process_company, company)


def process_company(company):
    print("Thread started...")
    print(f"Processing company: {company[0]}")
    start_time = time.time()

    if company[1] is None:
        get_10_year_data(company[0])
    elif company[1] != date.today():
        get_missing_data(company[0], company[1])

    end_time = time.time()
    execution_time = end_time - start_time
    print("Thread finished in {} seconds".format(execution_time))


def filter_1(url):
    response = requests.get(url)
    raw_html = response.text
    soup = BeautifulSoup(raw_html, "html.parser")
    select_menu = soup.find('select', class_='form-control')
    options = [option.get_text(strip=True) for option in select_menu.find_all('option')]
    filtered_options = []
    for option in options:
        if option.isalpha():
            filtered_options.append(option)
            save_company(option)
            # c = Company(
            #     name=option
            # )
            # c.save()

    return filtered_options


def filter_1_corrected(url):
    response = requests.get(url)
    raw_html = response.text
    soup = BeautifulSoup(raw_html, "html.parser")

    tbodies = soup.find_all('tbody')
    filtered_options = []

    for tbody in tbodies:
        for row in tbody.find_all('tr'):
            symbol_tag = row.find('a')
            if symbol_tag:
                symbol = symbol_tag.get_text(strip=True)
                if symbol.isalpha() and symbol not in filtered_options:
                    filtered_options.append(symbol)

    return filtered_options


def filter_2(companies):
    companies_last_dates = [get_last_date_string(company) for company in companies]
    return companies_last_dates


def filter_3(companies_last_dates):
    num_cores = os.cpu_count()
    max_workers = num_cores

    with Manager() as manager:

        start_time = time.time()
        print("Starting scraping data from MSE...")

        chunk_size = len(companies_last_dates) // num_cores
        company_chunks = [companies_last_dates[i:i + chunk_size] for i in range(0, len(companies_last_dates), chunk_size)]

        processes = []
        for chunk in company_chunks:
            p = Process(target=worker, args=(chunk, max_workers))
            processes.append(p)
            p.start()

        for p in processes:
            p.join()

        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Total execution time: {execution_time:.2f} seconds")


if __name__ == '__main__':
    # start_time = time.time()
    # companies = filter_1("https://www.mse.mk/mk/stats/symbolhistory/KMB")
    # data = filter_2(companies)
    # filter_3(data)
    # end_time = time.time()
    # execution_time = end_time - start_time
    # print(f"Total execution time: {execution_time:.2f} seconds")
    comp = filter_1("https://www.mse.mk/mk/stats/symbolhistory/KMB")
    print(len(comp))