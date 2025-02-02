import torch
from torch.utils.data import DataLoader, Dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, DataCollatorWithPadding, get_scheduler
from sklearn.metrics import classification_report
from tqdm import tqdm
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MSEDataAnalising.settings')
django.setup()
from ...NLP.models import News

device = "cuda" if torch.cuda.is_available() else "cpu"
torch.cuda.empty_cache()

tokenizer = AutoTokenizer.from_pretrained("AnkitAI/distilbert-base-uncased-financial-news-sentiment-analysis")
model = AutoModelForSequenceClassification.from_pretrained(
    "AnkitAI/distilbert-base-uncased-financial-news-sentiment-analysis",
    num_labels=3  # Three labels: 0=negative, 1=positive, 2=neutral
).to(device)

label_map = {"negative": 0, "positive": 1, "neutral": 2}

# Custom dataset class
class NewsDataset(Dataset):
    def __init__(self, news_entries, tokenizer, label_map):
        self.news_entries = news_entries
        self.tokenizer = tokenizer
        self.label_map = label_map

    def __len__(self):
        return len(self.news_entries)

    def __getitem__(self, idx):
        news_entry = self.news_entries[idx]
        content = news_entry.content
        label = self.label_map[news_entry.sentiment.lower()]
        inputs = self.tokenizer(content, truncation=True, padding="max_length", max_length=128)
        return {**inputs, "labels": torch.tensor(label)}

all_news_entries = list(News.objects.all())
train_size = int(0.8 * len(all_news_entries))
train_news_entries = all_news_entries[:train_size]
valid_news_entries = all_news_entries[train_size:]

train_dataset = NewsDataset(train_news_entries, tokenizer, label_map)
valid_dataset = NewsDataset(valid_news_entries, tokenizer, label_map)

data_collator = DataCollatorWithPadding(tokenizer=tokenizer)
train_loader = DataLoader(train_dataset, shuffle=True, batch_size=16, collate_fn=data_collator)
valid_loader = DataLoader(valid_dataset, batch_size=16, collate_fn=data_collator)

optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5)
num_training_steps = 3 * len(train_loader)  # 3 epochs
lr_scheduler = get_scheduler("linear", optimizer=optimizer, num_warmup_steps=0, num_training_steps=num_training_steps)

model.train()
epochs = 3

for epoch in range(epochs):
    loop = tqdm(train_loader, leave=True)
    for batch in loop:
        batch = {k: v.to(device) for k, v in batch.items()}

        outputs = model(**batch)
        loss = outputs.loss
        loss.backward()

        optimizer.step()
        lr_scheduler.step()
        optimizer.zero_grad()

        loop.set_description(f"Epoch {epoch}")
        loop.set_postfix(loss=loss.item())

model.eval()
predictions, true_labels = [], []

with torch.no_grad():
    for batch in valid_loader:
        batch = {k: v.to(device) for k, v in batch.items()}
        outputs = model(**batch)
        logits = outputs.logits
        predictions.extend(torch.argmax(logits, axis=1).cpu().numpy())
        true_labels.extend(batch["labels"].cpu().numpy())

print(classification_report(true_labels, predictions, target_names=["negative", "positive", "neutral"]))

# Save the fine-tuned model
model.save_pretrained("trained_models/fine_tuned_financial_sentiment_model_db_5")
tokenizer.save_pretrained("trained_models/fine_tuned_financial_sentiment_model_db_5")
torch.cuda.empty_cache()