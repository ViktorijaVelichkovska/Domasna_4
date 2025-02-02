import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import os
import django
from concurrent.futures import ThreadPoolExecutor
import time
from ..NLP.models import News, Company
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MSEDataAnalising.settings')
django.setup()

device = "cuda" if torch.cuda.is_available() else "cpu"

model_path = "trained_models/fine_tuned_financial_sentiment_model_db_5"
model = AutoModelForSequenceClassification.from_pretrained(model_path).to(device)
tokenizer = AutoTokenizer.from_pretrained(model_path)


def predict(text):
    inputs = tokenizer(text, truncation=True, padding="max_length", max_length=128, return_tensors="pt").to(device)

    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits

    probabilities = torch.nn.functional.softmax(logits, dim=-1)
    labels = ["negative", "positive", "neutral"]
    scores = {label: probabilities[0][i].item() for i, label in enumerate(labels)}
    return scores


def process_company_news(company_code):
    try:
        company_news = News.objects.filter(company_code=company_code).order_by('-date')[:30]

        if not company_news.exists():
            return {"company_code": company_code, "average_sentiment": None}

        aggregated_scores = {"positive": 0, "negative": 0, "neutral": 0}
        for news_entry in company_news:
            sentiment_scores = predict(news_entry.content)
            for key, value in sentiment_scores.items():
                aggregated_scores[key] += value

        count = len(company_news)
        average_scores = {key: value / count for key, value in aggregated_scores.items()}

        max_sentiment_type = max(average_scores, key=average_scores.get)
        max_sentiment_value = average_scores[max_sentiment_type]

        company, created = Company.objects.update_or_create(
            company_code=company_code,
            defaults={
                "max_sentiment": max_sentiment_type,
                "max_sentiment_value": max_sentiment_value
            }
        )

        if created:
            print(f"Created new company record: {company}")
        else:
            print(f"Updated company record: {company}")

        return {"company_code": company_code, "average_sentiment": average_scores}

    except Exception as e:
        print(f"Error processing company {company_code}: {e}")
        return {"company_code": company_code, "average_sentiment": None}


def process_all_companies(company_codes, num_threads):
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        results = list(executor.map(process_company_news, company_codes))
    return results


if __name__ == "__main__":
    start_time = time.time()

    num_threads = os.cpu_count()

    company_codes = (
        News.objects.exclude(company_code__isnull=True)
        .exclude(company_code="")
        .values_list("company_code", flat=True)
    )
    unique_company_codes = list(set(company_codes))
    unique_company_codes.sort()

    results = process_all_companies(unique_company_codes, num_threads)

    for result in results:
        print(f"Company Code: {result['company_code']}, Average Sentiment: {result['average_sentiment']}")
    # for c in company_codes:
    #     company_news = News.objects.filter(company_code=c).order_by('-date')[:1]
    #     Company.objects.filter(company_code=c).update(company_name=company_news[0].company_name)
    #

    end_time = time.time()
    print(f"Total execution time: {end_time - start_time:.2f} seconds")
    print("Processing complete.")
    torch.cuda.empty_cache()