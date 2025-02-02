import matplotlib.pyplot as plt


def plot_technical_analysis(data):
    """
    Креира график со техничка анализа и сигнали.

    :param data: Pandas DataFrame со обработени податоци.
    """
    plt.figure(figsize=(12, 6))
    plt.plot(data['date'], data['last_transaction_price'], label='Price', color='blue')
    plt.plot(data['date'], data['SMA_5'], label='SMA 5', color='green')
    plt.plot(data['date'], data['EMA_5'], label='EMA 5', color='orange')

    # Додавање сигнали на графикот
    buy_signals = data[data['Signal'] == 'Buy']
    sell_signals = data[data['Signal'] == 'Sell']
    plt.scatter(buy_signals['date'], buy_signals['last_transaction_price'], label='Buy Signal', marker='^',
                color='green')
    plt.scatter(sell_signals['date'], sell_signals['last_transaction_price'], label='Sell Signal', marker='v',
                color='red')

    plt.legend()
    plt.title('Technical Analysis with Signals')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.grid()
    plt.show()
