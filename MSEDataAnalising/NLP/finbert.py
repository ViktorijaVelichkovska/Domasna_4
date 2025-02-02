import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import os
import django
from concurrent.futures import ThreadPoolExecutor
import time
from ..NLP.models import News
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MSEDataAnalising.settings')
django.setup()

device = "cuda" if torch.cuda.is_available() else "cpu"

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis")
model = AutoModelForSequenceClassification.from_pretrained(
    "mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis"
)
model.to(device)
model.eval()

# Fetch all news entries (example limit of 10)
all_news_entries = News.objects.all()

def predict_sentiment(news_entry):
    try:
        # Tokenize input (headline)
        input = tokenizer(news_entry.content, padding=True, truncation=True, return_tensors='pt').to(device)

        # Inference
        with torch.no_grad():
            outputs = model(**input)

        predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)

        sentiment_scores = {
            "positive": predictions[0][0].item(),
            "negative": predictions[0][1].item(),
            "neutral": predictions[0][2].item()
        }
        max_sentiment = max(sentiment_scores, key=sentiment_scores.get)

        news_entry.sentiment = max_sentiment
        news_entry.save()
        print(f"{news_entry.id} - {news_entry.sentiment}")

    except RuntimeError as e:
        print(f"Error processing news entry {news_entry.id}: {e}")
        torch.cuda.empty_cache()

def process_news_entries(news_entries):
    with ThreadPoolExecutor() as executor:
        executor.map(predict_sentiment, news_entries)



start_time = time.time()
all_news_entries = News.objects.all()
num_threads = os.cpu_count()
process_news_entries(all_news_entries)

torch.cuda.empty_cache()

end_time = time.time()
print(f"Total execution time: {end_time - start_time:.2f} seconds")