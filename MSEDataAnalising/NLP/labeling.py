import os
import django
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Process, cpu_count
import time
from ..NLP.models import News

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MSEDataAnalising.settings')
django.setup()

positive_keywords = [
    'success', 'positive', 'growth', 'good', 'profit', 'gain', 'revenue', 'increase',
    'achievement', 'improvement', 'expansion', 'surplus', 'investment', 'rise',
    'opportunity', 'advancement', 'prosperity', 'dividend', 'return', 'stability',
    'boom', 'high', 'outperformance', 'record', 'bullish', 'upgrade', 'strong',
    'breakthrough', 'milestone', 'new high', 'leader', 'competitive advantage',
    'partnership', 'buyback', 'market share', 'efficiency', 'demand', 'positive trend',
    'growth rate', 'overachievement', 'innovation', 'product launch', 'earnings beat'
]

negative_keywords = [
    'fall', 'failure', 'increased', 'expenses', 'problem', 'bad', 'loss', 'decline',
    'decrease', 'deficit', 'drop', 'recession', 'debt', 'risk', 'cut', 'layoff',
    'crisis', 'uncertainty', 'downturn', 'slowdown', 'collapse', 'low', 'instability',
    'losses', 'challenge', 'underperformance', 'downgrade', 'bearish', 'competition',
    'headwinds', 'volatility', 'miss', 'fraud', 'bankruptcy', 'shortfall',
    'litigation', 'scandal', 'overvaluation', 'delisting', 'default', 'profit warning',
    'loss of market share', 'negative trend', 'inefficiency', 'cost increase'
]

neutral_keywords = [
    'information', 'report', 'agreement', 'action', 'meeting', 'announcement',
    'update', 'plan', 'forecast', 'strategy', 'discussion', 'conference', 'decision',
    'statement', 'policy', 'target', 'agenda', 'analysis', 'regulation',
    'statistics', 'projections', 'status', 'overview', 'results', 'survey',
    'guidance', 'outlook', 'expectations', 'market movement', 'price action',
    'regulatory filing', 'news release', 'earnings call', 'press release',
    'corporate action', 'merger', 'acquisition', 'IPO', 'spin-off', 'shareholder meeting',
    'capital raise', 'dividend policy', 'stock split', 'insider trading'
]

def classify_text(text):
    text = text.lower()

    if any(word in text for word in positive_keywords):
        return 'Positive'
    elif any(word in text for word in negative_keywords):
        return 'Negative'
    elif any(word in text for word in neutral_keywords):
        return 'Neutral'
    else:
        return 'Neutral'

def process_chunk(news_entries):
    def classify_and_save(news_entry):
        sentiment = classify_text(news_entry.content)
        news_entry.sentiment = sentiment
        news_entry.save()
        print(f"{news_entry.id} - {sentiment}")

    with ThreadPoolExecutor() as executor:
        executor.map(classify_and_save, news_entries)

def distribute_work(all_news_entries, num_processes):

    chunk_size = len(all_news_entries) // num_processes
    processes = []

    for i in range(num_processes):
        start_idx = i * chunk_size
        end_idx = (i + 1) * chunk_size if i != num_processes - 1 else len(all_news_entries)
        chunk = all_news_entries[start_idx:end_idx]
        process = Process(target=process_chunk, args=(chunk,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

if __name__ == '__main__':
    start_time = time.time()

    all_news_entries = list(News.objects.all())
    num_processes = min(cpu_count(), 4)
    distribute_work(all_news_entries, num_processes)

    end_time = time.time()
    print(f"Total execution time: {end_time - start_time:.2f} seconds")