import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Process
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MSEDataAnalising.settings')
django.setup()

from ..NLP.models import News


def get_page_count():
    url = "https://www.mse.mk/en/news/latest/1"

    response = requests.get(url)

    last_page_number = -1

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        links = soup.findAll('a')

        for link in links:
            if link.text.strip() == 'Last':
                last_page_number = int(link['href'].split('/')[-1])
    else:
        print("Failed to fetch the page.")

    return last_page_number


def get_page_links_worker(pages_subset, stop_date):
    with ThreadPoolExecutor(max_workers=4) as executor:
        for page in pages_subset:
            executor.submit(process_page, page, stop_date)


def process_page(page, stop_date):
    base_url = "https://www.mse.mk/en/news/latest/"
    url = f"{base_url}{page}"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        rows = soup.findAll('div', class_='row')
        for row in rows:
            if row.find('a') is not None:
                news_date_str = row.find('a').text.strip()
                try:
                    news_date = datetime.strptime(news_date_str, "%m/%d/%Y")
                except ValueError:
                    print(f"Could not parse date: {news_date_str}")
                    continue

                title = row.find(class_='col-md-11').find('a').text.strip()
                link = f"https://www.mse.mk{row.find(class_='col-md-1').find('a')['href']}"
                print(f"News date: {news_date_str}")
                print(f"News link: {link}")
                print(title)
                content = get_news_content(link)
                if content is not None and len(content) > 0:
                    save_news_to_model(news_date, title, link, content)
    else:
        print(f"Failed to fetch page {page}")


def get_news_content(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        content_div = soup.find('div', id='content')

        if content_div:
            paragraphs = content_div.find_all('p')
            content = "\n".join(paragraph.text.strip() for paragraph in paragraphs)
            return content
        else:
            print(f"No content found on {url}")
            return None
    else:
        print(f"Failed to fetch the page {url}")
        return None


def save_news_to_model(news_date, title, link, content):
    if not News.objects.filter(title=title, date=news_date).exists():
        news_entry = News.objects.create(
            date=news_date,
            title=title,
            link=link,
            content=content
        )
        print(f"Saved: {news_entry}")
        print(f"News with title '{title}' and date '{news_date}' saved!")

    else:
        print(f"News with title '{title}' and date '{news_date}' already exists. Skipping...")


def get_page_links_multiprocessing(last_page_number, stop_date):
    num_cores = os.cpu_count()
    chunk_size = (last_page_number - 1) // num_cores
    page_chunks = [range(i, i + chunk_size) for i in range(1, last_page_number, chunk_size)]

    processes = []
    for chunk in page_chunks:
        p = Process(target=get_page_links_worker, args=(chunk, stop_date))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()


if __name__ == "__main__":
    stop_date = datetime.today() - timedelta(weeks=20)
    page_count = get_page_count()

    if page_count > 0:
        get_page_links_multiprocessing(page_count, stop_date)