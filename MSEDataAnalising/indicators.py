import pandas as pd
import numpy as np

def calculate_indicators(data):

    data['last_transaction_price'] = data['last_transaction_price'].replace({',': ''}, regex=True).astype(float)
    data['min_price'] = data['min_price'].replace({',': ''}, regex=True).astype(float)
    data['max_price'] = data['max_price'].replace({',': ''}, regex=True).astype(float)

    #Moving Averages
    timeframes = {'1_day': 1, '1_week': 7, '1_month': 30}
    for key, window in timeframes.items():
        #SMA
        data[f'SMA_{key}'] = data['last_transaction_price'].rolling(window=window).mean()

        #EMA
        data[f'EMA_{key}'] = data['last_transaction_price'].ewm(span=window, adjust=False).mean()

        #WMA
        data[f'WMA_{key}'] = data['last_transaction_price'].rolling(window=window).apply(
            lambda x: np.dot(x, np.arange(1, len(x)+1)) / np.sum(np.arange(1, len(x)+1)), raw=True)

        #HMA
        wma_short = data['last_transaction_price'].rolling(window=max(1, window//2)).apply(
            lambda x: np.dot(x, np.arange(1, len(x)+1)) / np.sum(np.arange(1, len(x)+1)), raw=True)
        wma_long = data['last_transaction_price'].rolling(window=window).apply(
            lambda x: np.dot(x, np.arange(1, len(x)+1)) / np.sum(np.arange(1, len(x)+1)), raw=True)
        data[f'HMA_{key}'] = 2 * wma_short - wma_long

        #TMA
        data[f'TMA_{key}'] = data['last_transaction_price'].rolling(window=window).mean().rolling(window=window).mean()

    #Oscillators
    for key, window in timeframes.items():
        # RSI
        delta = data['last_transaction_price'].diff()
        gain = np.where(delta > 0, delta, 0)
        loss = np.where(delta < 0, -delta, 0)
        avg_gain = pd.Series(gain).rolling(window=window).mean()
        avg_loss = pd.Series(loss).rolling(window=window).mean()
        rs = avg_gain / avg_loss
        data[f'RSI_{key}'] = 100 - (100 / (1 + rs))

        #Stochastic Oscillator
        data[f'Stochastic_{key}'] = ((data['last_transaction_price'] - data['min_price'].rolling(window).min()) /
                                     (data['max_price'].rolling(window).max() - data['min_price'].rolling(window).min())) * 100

        #MACD
        ema_12 = data['last_transaction_price'].ewm(span=12, adjust=False).mean()
        ema_26 = data['last_transaction_price'].ewm(span=26, adjust=False).mean()
        data[f'MACD_{key}'] = ema_12 - ema_26

        #CCI
        tp = (data['last_transaction_price'] + data['max_price'] + data['min_price']) / 3
        sma = tp.rolling(window=window).mean()
        mad = tp.rolling(window=window).apply(lambda x: np.mean(np.abs(x - x.mean())))
        data[f'CCI_{key}'] = (tp - sma) / (0.015 * mad)

        #Williams %R
        data[f'WilliamsR_{key}'] = ((data['max_price'].rolling(window).max() - data['last_transaction_price']) /
                                    (data['max_price'].rolling(window).max() - data['min_price'].rolling(window).min())) * -100

    #signals
    data['Signal'] = 'Hold'
    for key in timeframes.keys():
        #Buy: Ако цената е над SMA и EMA за соодветната временска рамка
        data.loc[data['last_transaction_price'] > data[f'SMA_{key}'], 'Signal'] = 'Buy'
        #Sell: Ако цената е под EMA за соодветната временска рамка
        data.loc[data['last_transaction_price'] < data[f'EMA_{key}'], 'Signal'] = 'Sell'

    return data



file_path = "../../../MSEDataAnalising/servisi/LSTM/lstmmm/combined_data.csv"
data = pd.read_csv(file_path)


data_with_indicators = calculate_indicators(data)


output_path = "indicators_with_signals.csv"
data_with_indicators.to_csv(output_path, index=False, float_format='%.2f')

print(f"Резултатите се зачувани во {output_path}.")
print(data_with_indicators.head())
