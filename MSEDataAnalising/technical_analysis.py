import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('../../../MSEDataAnalising/servisi/LSTM/lstmmm/combined_data.csv')


df['last_transaction_price'] = df['last_transaction_price'].replace({',': '.'}, regex=True)  # Замени запирки со точки
df['last_transaction_price'] = df['last_transaction_price'].replace({'\\.' : ''}, regex=True)  # Отстрани точките за илјадници
df['last_transaction_price'] = df['last_transaction_price'].astype(float)  # Конвертирај во float


df['SMA_1_day'] = df['last_transaction_price'].rolling(window=1).mean()
df['SMA_7_day'] = df['last_transaction_price'].rolling(window=7).mean()
df['SMA_30_day'] = df['last_transaction_price'].rolling(window=30).mean()


df['EMA_1_day'] = df['last_transaction_price'].ewm(span=1, adjust=False).mean()
df['EMA_7_day'] = df['last_transaction_price'].ewm(span=7, adjust=False).mean()
df['EMA_30_day'] = df['last_transaction_price'].ewm(span=30, adjust=False).mean()


delta = df['last_transaction_price'].diff()
gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
rs = gain / loss
df['RSI_14'] = 100 - (100 / (1 + rs))

#MACD
ema_12 = df['last_transaction_price'].ewm(span=12, adjust=False).mean()
ema_26 = df['last_transaction_price'].ewm(span=26, adjust=False).mean()
df['MACD'] = ema_12 - ema_26
df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()

#Bollinger Bands
df['BB_upper'] = df['SMA_1_day'] + (df['last_transaction_price'].rolling(window=14).std() * 2)
df['BB_lower'] = df['SMA_1_day'] - (df['last_transaction_price'].rolling(window=14).std() * 2)

#signals
def generate_signals(row):
    if row['last_transaction_price'] > row['BB_upper']:
        return 'Sell'
    elif row['last_transaction_price'] < row['BB_lower']:
        return 'Buy'
    else:
        return 'Hold'

df['Signal'] = df.apply(generate_signals, axis=1)


print(df[['date', 'last_transaction_price', 'SMA_1_day', 'SMA_7_day', 'SMA_30_day', 'EMA_1_day', 'EMA_7_day', 'EMA_30_day', 'RSI_14', 'MACD', 'Signal_Line', 'BB_upper', 'BB_lower', 'Signal']])


df.to_csv('technical_analysis_results.csv', index=False)


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


df.to_csv('technical_analysis_results.csv', index=False)

print(df.head())
