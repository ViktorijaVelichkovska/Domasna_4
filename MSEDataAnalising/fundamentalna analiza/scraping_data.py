import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Process
import django

# Поставување на Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MSEDataAnalising.settings')
django.setup()

from NLP import News

class MSEDataScraper:
    def __init__(self, stop_date=None):
        self.base_url = "https://www.mse.mk/en/news/latest/"
        self.stop_date = stop_date or (datetime.today() - timedelta(weeks=20))

    def get_page_count(self):
        url = f"{self.base_url}1"
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

    def get_page_links_worker(self, pages_subset):
        with ThreadPoolExecutor(max_workers=4) as executor:
            for page in pages_subset:
                executor.submit(self.process_page, page)

    def process_page(self, page):
        url = f"{self.base_url}{page}"
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            rows = soup.findAll('div', class_='row')
            for row in rows:
                if row.find('a') is not None:
                    self.process_news_row(row)
        else:
            print(f"Failed to fetch page {page}")

    def process_news_row(self, row):
        news_date_str = row.find('a').text.strip()
        try:
            news_date = datetime.strptime(news_date_str, "%m/%d/%Y")
        except ValueError:
            print(f"Could not parse date: {news_date_str}")
            return

        title = row.find(class_='col-md-11').find('a').text.strip()
        link = f"https://www.mse.mk{row.find(class_='col-md-1').find('a')['href']}"
        print(f"News date: {news_date_str}")
        print(f"News link: {link}")
        print(title)

        content = self.get_news_content(link)
        if content:
            self.save_news_to_model(news_date, title, link, content)

    def get_news_content(self, url):
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            content_div = soup.find('div', id='content')

            if content_div:
                paragraphs = content_div.find_all('p')
                content = "\n".join(paragraph.text.strip() for paragraph in paragraphs)
                return content
        else:
            print(f"Failed to fetch the page {url}")
        return None

    def save_news_to_model(self, news_date, title, link, content):
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

    def get_page_links_multiprocessing(self, last_page_number):
        num_cores = os.cpu_count()
        chunk_size = (last_page_number - 1) // num_cores
        page_chunks = [range(i, i + chunk_size) for i in range(1, last_page_number, chunk_size)]

        processes = []
        for chunk in page_chunks:
            p = Process(target=self.get_page_links_worker, args=(chunk,))
            processes.append(p)
            p.start()

        for p in processes:
            p.join()

    def run(self):
        page_count = self.get_page_count()
        if page_count > 0:
            self.get_page_links_multiprocessing(page_count)


if __name__ == "__main__":
    scraper = MSEDataScraper()
    scraper.run()
