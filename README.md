# Domasna_4

1 Рефакторирање на кодот:
Нашиот код може да се рефакторира со имплементација на Стратегискиот шаблон (Strategy Pattern) за пресметка на техничките индикатори.

Кодот од TechnicalAnalysis рефакториран:

import pandas as pd
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod

class TechnicalIndicator(ABC):
    @abstractmethod
    def calculate(self, df):
        pass

class SimpleMovingAverage(TechnicalIndicator):
    def __init__(self, window):
        self.window = window
    
    def calculate(self, df):
        return df['last_transaction_price'].rolling(window=self.window).mean()

class ExponentialMovingAverage(TechnicalIndicator):
    def __init__(self, span):
        self.span = span
    
    def calculate(self, df):
        return df['last_transaction_price'].ewm(span=self.span, adjust=False).mean()

class RSIIndicator(TechnicalIndicator):
    def __init__(self, window=14):
        self.window = window
    
    def calculate(self, df):
        delta = df['last_transaction_price'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=self.window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=self.window).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

class MACDIndicator(TechnicalIndicator):
    def calculate(self, df):
        ema_12 = df['last_transaction_price'].ewm(span=12, adjust=False).mean()
        ema_26 = df['last_transaction_price'].ewm(span=26, adjust=False).mean()
        macd = ema_12 - ema_26
        signal_line = macd.ewm(span=9, adjust=False).mean()
        return macd, signal_line

class BollingerBands(TechnicalIndicator):
    def __init__(self, window=14):
        self.window = window
    
    def calculate(self, df):
        sma = df['last_transaction_price'].rolling(window=self.window).mean()
        std = df['last_transaction_price'].rolling(window=self.window).std()
        upper_band = sma + (std * 2)
        lower_band = sma - (std * 2)
        return upper_band, lower_band

def generate_signals(row):
    if row['last_transaction_price'] > row['BB_upper']:
        return 'Sell'
    elif row['last_transaction_price'] < row['BB_lower']:
        return 'Buy'
    else:
        return 'Hold'

# Load data
df = pd.read_csv('../../../MSEDataAnalising/LSTM/lstm/combined_data.csv')
df['last_transaction_price'] = df['last_transaction_price'].replace({',': '.'}, regex=True)
df['last_transaction_price'] = df['last_transaction_price'].replace({'\\.': ''}, regex=True)
df['last_transaction_price'] = df['last_transaction_price'].astype(float)

# Calculate indicators
sma_7 = SimpleMovingAverage(7)
sma_30 = SimpleMovingAverage(30)
ema_7 = ExponentialMovingAverage(7)
ema_30 = ExponentialMovingAverage(30)
rsi = RSIIndicator()
macd = MACDIndicator()
bb = BollingerBands()

df['SMA_7_day'] = sma_7.calculate(df)
df['SMA_30_day'] = sma_30.calculate(df)
df['EMA_7_day'] = ema_7.calculate(df)
df['EMA_30_day'] = ema_30.calculate(df)
df['RSI_14'] = rsi.calculate(df)
df['MACD'], df['Signal_Line'] = macd.calculate(df)
df['BB_upper'], df['BB_lower'] = bb.calculate(df)

df['Signal'] = df.apply(generate_signals, axis=1)

df.to_csv('technical_analysis_results.csv', index=False)

# Plot results
plt.figure(figsize=(12, 6))
plt.plot(df['last_transaction_price'], label='Last Transaction Price', color='blue')
plt.plot(df['SMA_7_day'], label='SMA 7 Day', color='orange')
plt.plot(df['SMA_30_day'], label='SMA 30 Day', color='green')
plt.fill_between(range(len(df)), df['BB_upper'], df['BB_lower'], color='gray', alpha=0.2, label='Bollinger Bands')
plt.legend(loc='best')
plt.title('Stock Analysis with SMA, EMA, MACD, RSI, and Bollinger Bands')
plt.xlabel('Index')
plt.ylabel('Price')
plt.grid()
plt.savefig('technical_analysis_plot.png')
plt.close()

print(df.head())

Рефакторираниов код го следи шаблонот Strategy, овозможувајќи лесно додавање и модифицирање на различни технички индикатори. Овој пристап го подобрува читањето, одржувањето и повторната употребливост на кодот.

Во оваа веб-апликација, имплементиравме архитектонскиот шаблон MVP (Model-View-Presenter).

View

React е задолжен за прикажување на корисничкиот интерфејс, нудејќи динамична и интуитивна визуелизација на податоците.

Model

Django ја управува базата на податоци и бизнис логиката. Контролерите (API-ите) испраќаат JSON одговори на клиентските барања, овозможувајќи сигурно и структуирано управување со податоците.


Presenter

Во нашата имплементација, React ја презема улогата на Презентер, каде што:
•	Ги обработува корисничките интеракции (кликања, селекции, внесување податоци).
•	Испраќа HTTP барања до Django backend за добивање и ажурирање на податоци.
•	Ги складира и трансформира добиените JSON податоци пред да ги прикаже во UI.

