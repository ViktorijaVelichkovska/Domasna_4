import os
import django
import pandas as pd

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MSEDataAnalising.MSEDataAnalising.settings')
django.setup()


from datascraper.serializers import DayEntryAsStringSerializer, DayEntryAsString

def clean_data(data):
    data['last_transaction_price'] = data['last_transaction_price'].str.replace('.', '').str.replace(',', '.')
    data['last_transaction_price'] = pd.to_numeric(data['last_transaction_price'], errors='coerce')
    data['max_price'] = data['max_price'].str.replace('.', '').str.replace(',', '.')
    data['max_price'] = pd.to_numeric(data['max_price'], errors='coerce')
    data['min_price'] = data['min_price'].str.replace('.', '').str.replace(',', '.')
    data['min_price'] = pd.to_numeric(data['min_price'], errors='coerce')
    data['date'] = pd.to_datetime(data['date'], errors='coerce')
    data = data.sort_values(by='date', ascending=True).reset_index(drop=True)
    data.set_index('date', inplace=True)
    data['max_price'] = data['max_price'].ffill()
    data['min_price'] = data['min_price'].ffill()
    return data

def process_company_data(company_code, indicators, freqs=['1D', '1W', '1ME']):
    """
    Process stock data for a given company, calculate indicators, and generate signals.
    """
    entries = DayEntryAsString.objects.filter(company_code=company_code)
    serializer = DayEntryAsStringSerializer(entries, many=True)
    data = pd.DataFrame(serializer.data)

    data = clean_data(data)
    missing_entries, missing_percentage = calculate_missing_entries(data)
    if missing_percentage > 20:
        raise ValueError(f"Company {company_code} has too much missing data (over 20%). Skipping analysis.")

    results = {}

    for freq in freqs:
        if freq != '1D':
            resampled_data = resample_data(data, freq)
        else:
            resampled_data = data

        resampled_data = calculate_moving_averages(resampled_data, indicators)
        resampled_data = generate_signals(resampled_data, indicators)

        results[freq] = resampled_data

    return results


def calculate_moving_averages(data, indicators):
    """
    Calculate various moving averages and other indicators.
    """
    for indicator in indicators:
        if 'SMA' in indicator:
            window = int(indicator.split('(')[1].strip(')'))
            data[indicator] = data['last_transaction_price'].rolling(window=window).mean()
        elif 'EMA' in indicator:
            span = int(indicator.split('(')[1].strip(')'))
            data[indicator] = data['last_transaction_price'].ewm(span=span, adjust=False).mean()
        elif indicator == 'Ichimoku_Baseline':
            data[indicator] = (
                data['max_price'].rolling(window=26).max() +
                data['min_price'].rolling(window=26).min()
            ) / 2
    return data

def generate_signals(data, indicators, threshold=0.1):
    """
    Generate Buy/Sell/Hold signals with thresholds to reduce noise.
    """
    for indicator in indicators:
        signal_column = f'Signal_{indicator}'
        data[signal_column] = 'Hold'

        buy_condition = data['last_transaction_price'] > (1 + threshold) * data[indicator]
        sell_condition = data['last_transaction_price'] < (1 - threshold) * data[indicator]

        data.loc[buy_condition, signal_column] = 'Buy'
        data.loc[sell_condition, signal_column] = 'Sell'

    return data



def resample_data(data, freq):
    resampled_data = data.resample(freq).agg({
        'last_transaction_price': 'mean',
        'max_price': 'max',
        'min_price': 'min'
    })

    if resampled_data['last_transaction_price'].isnull().any():
        resampled_data['last_transaction_price'] = resampled_data[
            'last_transaction_price'].ffill()
        print(f'null in last_tran in {freq}')
    if resampled_data['max_price'].isnull().any():
        resampled_data['max_price'] = resampled_data['max_price'].ffill()
        print(f'null in max in {freq}')
    if resampled_data['min_price'].isnull().any():
        resampled_data['min_price'] = resampled_data['min_price'].ffill()
        print(f'null in min in {freq}')

    return resampled_data


def calculate_missing_entries(df, total_entries=2520):
    actual_entries = len(df)
    missing_entries = total_entries - actual_entries
    missing_percentage = (missing_entries / total_entries) * 100

    return missing_entries, missing_percentage

if __name__ == '__main__':
    company_code = 'KMB'
    indicators = ['SMA(50)', 'SMA(200)', 'EMA(50)', 'EMA(200)', 'Ichimoku_Baseline']
    freqs = ['1D', '1W', '1ME']

    try:
        processed_data = process_company_data(company_code, indicators, freqs)
        pd.set_option('display.max_columns', None)
        print(processed_data['1D'].tail(1))  # Example: Last row of daily data
    except ValueError as e:
        print(f"Error: {e}")