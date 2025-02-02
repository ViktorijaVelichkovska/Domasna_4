import os
import django
import pandas as pd
import ta
from LSTM.lstm.oscilators.models import DayEntryAsString
# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MSEDataAnalising.settings')
django.setup()

from datascraper.serializers import DayEntryAsStringSerializer


def process_company_data(company_code, indicators=['RSI', 'stoch_k', 'cci', 'macd', 'adx'], freqs=['1D', '1W', '1ME'],
                         window=14, smooth_window=None):
    entries = DayEntryAsString.objects.filter(company_code=company_code)
    serializer = DayEntryAsStringSerializer(entries, many=True)
    data = serializer.data

    df = pd.DataFrame(data)

    df = clean_data(df)

    missing_entries, missing_percentage = calculate_missing_entries(df)

    print(f"Missing entries: {missing_entries}")
    print(f"Missing percentage: {missing_percentage:.2f}%")

    if missing_percentage > 20:
        raise ValueError(f"Company {company_code} has too much missing data (over 20%). Skipping analysis.")

    results = {}

    for freq in freqs:
        if freq != '1D':
            resampled_data = resample_data(df, freq)
        else:
            resampled_data = df

        for indicator in indicators:
            resampled_data = calculate_indicator(resampled_data, indicator, window, smooth_window)

        for indicator in indicators:
            if indicator == 'RSI':
                resampled_data = generate_signals(resampled_data, 'RSI', 30, 70)
            elif indicator == 'stoch_k':
                resampled_data = generate_signals(resampled_data, 'stoch_k', 20, 80)
            elif indicator == 'cci':
                resampled_data = generate_signals(resampled_data, 'cci', -100, 100)
            elif indicator == 'macd':
                resampled_data['Signal_macd'] = 'Hold'
                resampled_data.loc[resampled_data['macd'] > resampled_data['macd_signal'], 'Signal_macd'] = 'Buy'
                resampled_data.loc[resampled_data['macd'] < resampled_data['macd_signal'], 'Signal_macd'] = 'Sell'
            elif indicator == 'adx':
                resampled_data['Signal_adx'] = 'Hold'
                resampled_data.loc[(resampled_data['+di'] > resampled_data['-di']) & (
                            resampled_data['adx'] > 25), 'Signal_adx'] = 'Buy'
                resampled_data.loc[(resampled_data['-di'] > resampled_data['+di']) & (
                            resampled_data['adx'] > 25), 'Signal_adx'] = 'Sell'
                resampled_data.loc[resampled_data['adx'] < 25, 'Signal_adx'] = 'Hold'

        results[freq] = resampled_data

    return results


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


def generate_signals(data, indicator_column, buy_threshold, sell_threshold):
    data[f'Signal_{indicator_column}'] = 'Hold'
    data.loc[data[indicator_column] < buy_threshold, f'Signal_{indicator_column}'] = 'Buy'
    data.loc[data[indicator_column] > sell_threshold, f'Signal_{indicator_column}'] = 'Sell'
    return data


def calculate_indicator(data, indicator, window=14, smooth_window=None):
    if indicator == 'RSI':
        data['RSI'] = ta.momentum.RSIIndicator(data['last_transaction_price'], window=window).rsi()
    elif indicator == 'stoch_k':
        data['stoch_k'] = ta.momentum.StochasticOscillator(
            high=data['max_price'],
            low=data['min_price'],
            close=data['last_transaction_price'],
            window=window,
            smooth_window=smooth_window
        ).stoch()
    elif indicator == 'cci':
        data['cci'] = ta.trend.CCIIndicator(
            high=data['max_price'],
            low=data['min_price'],
            close=data['last_transaction_price'],
            window=window,
        ).cci()
    elif indicator == 'macd':
        macd = ta.trend.MACD(data['last_transaction_price'])
        data['macd'] = macd.macd()
        data['macd_signal'] = macd.macd_signal()
    elif indicator == 'adx':
        adx_indicator = ta.trend.ADXIndicator(
            high=data['max_price'],
            low=data['min_price'],
            close=data['last_transaction_price'],
            window=window
        )
        data['adx'] = adx_indicator.adx()
        data['+di'] = adx_indicator.adx_pos()
        data['-di'] = adx_indicator.adx_neg()
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
    # Example: print the results for each frequency
    company_code = 'ALK'
    indicators = ['RSI', 'stoch_k', 'cci', 'macd', 'adx']
    freqs = ['1D', '1W', '1ME']

    try:
        processed_data = process_company_data(company_code, indicators, freqs)
        for freq in freqs:
            print(f"\n{freq} сигнали:")
            print(processed_data[freq][
                      [f'Signal_RSI', f'Signal_stoch_k', f'Signal_cci', f'Signal_macd', f'Signal_adx']].tail(1))
    except ValueError as e:
        print(f"Error: {e}")