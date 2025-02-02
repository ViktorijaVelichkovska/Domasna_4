import os
import requests
import html
import re
import pdfplumber
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Process
import time
from html.parser import HTMLParser
import django

parser = HTMLParser()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MSEDataAnalising.settings')
django.setup()

from ..NLP.models import News


def process_document(document):
    content = document.get('content', '')
    document_id = document.get('documentId', '')
    description = document['layout']['description']
    content = html.unescape(content)
    content = re.sub(r'<[^>]*>', '', content)
    published_date = document['publishedDate'].split("T")[0]
    issuer_code = document['issuer']['code']
    display_name = document['issuer']['localizedTerms'][0]['displayName']

    if 'this is automaticaly generated document'.lower() in content.lower():
        print("The content is not available in English.")
        return

    text = ""
    attachments = document.get('attachments', [])
    if attachments:
        attachment_id = attachments[0].get('attachmentId')
        file_name = attachments[0].get('fileName')

        if file_name.lower().endswith('.pdf'):
            attachment_url = f"https://api.seinet.com.mk/public/documents/attachment/{attachment_id}"
            response = requests.get(attachment_url)
            if response.status_code == 200:
                pdf_file = BytesIO(response.content)
                with pdfplumber.open(pdf_file) as pdf:
                    for page in pdf.pages:
                        text += page.extract_text()
            content += "\n"
            content += text

    print(f"Issuer Code: {issuer_code}", flush=True)
    print(f"Content: {content}", flush=True)
    print(f"Published Date: {published_date}", flush=True)
    print(f"Description: {description}", flush=True)
    print(f"Display Name: {display_name}", flush=True)
    print(f"document_id: {document_id}", flush=True)
    print(" ")

    existing_entry = News.objects.filter(document_id=document_id).exists()

    if not existing_entry:
        try:
            new_entry = News.objects.create(
                document_id=document_id,
                date=published_date,
                description=description,
                content=content,
                company_code=issuer_code,
                company_name=display_name
            )
            print(f"New entry created: {new_entry}")
        except Exception as e:
            print(f"Error creating entry for document_id {document_id}: {e}")
    else:
        print(f"Entry with document_id {document_id} already exists. Skipping...")


def process_page(page):
    payload = {
        "issuerId": 0,
        "languageId": 2,
        "channelId": 1,
        "dateFrom": "2005-02-01T00:00:00",
        "dateTo": "2024-12-31T23:59:59",
        "isPushRequest": False,
        "page": page
    }
    headers = {"Content-Type": "application/json"}
    url = "https://api.seinet.com.mk/public/documents"

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        json_data = response.json()
        documents = json_data.get('data', [])
        with ThreadPoolExecutor(max_workers=4) as executor:
            for document in documents:
                executor.submit(process_document, document)
    else:
        print(f"Failed to fetch page {page}")


def fetch_pages_multiprocessing(total_pages, num_processes):
    processes = []
    chunk_size = total_pages // num_processes
    page_chunks = [range(i, min(i + chunk_size, total_pages + 1)) for i in range(1, total_pages + 1, chunk_size)]

    for chunk in page_chunks:
        p = Process(target=fetch_pages_worker, args=(chunk,))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()


def fetch_pages_worker(pages_subset):
    for page in pages_subset:
        process_page(page)


if __name__ == "__main__":
    # News.objects.all().delete()
    total_pages = 2694
    start_time = time.time()
    num_processes = os.cpu_count()

    fetch_pages_multiprocessing(total_pages, num_processes)

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Total execution time: {execution_time:.2f} seconds")
    print(f"Processing complete.")