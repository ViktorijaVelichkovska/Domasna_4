import ta
from LSTM.base_ta import IndicatorStrategy


# RSI Strategy
class RSIStrategy(IndicatorStrategy):
    def __init__(self, window):
        self.window = window

    def calculate(self, data):
        data['RSI'] = ta.momentum.RSIIndicator(data['last_transaction_price'], window=self.window).rsi()
        return data

    def generate_signals(self, data):
        data['Signal_RSI'] = 'Hold'
        data.loc[data['RSI'] < 30, 'Signal_RSI'] = 'Buy'
        data.loc[data['RSI'] > 70, 'Signal_RSI'] = 'Sell'
        return data


# Stochastic Oscillator Strategy
class StochKStrategy(IndicatorStrategy):
    def __init__(self, window, smooth_window=None):
        self.window = window
        self.smooth_window = smooth_window

    def calculate(self, data):
        data['stoch_k'] = ta.momentum.StochasticOscillator(
            high=data['max_price'],
            low=data['min_price'],
            close=data['last_transaction_price'],
            window=self.window,
            smooth_window=self.smooth_window
        ).stoch()
        return data

    def generate_signals(self, data):
        data['Signal_stoch_k'] = 'Hold'
        data.loc[data['stoch_k'] < 20, 'Signal_stoch_k'] = 'Buy'
        data.loc[data['stoch_k'] > 80, 'Signal_stoch_k'] = 'Sell'
        return data


# CCI Strategy
class CCIStrategy(IndicatorStrategy):
    def __init__(self, window):
        self.window = window

    def calculate(self, data):
        data['cci'] = ta.trend.CCIIndicator(
            high=data['max_price'],
            low=data['min_price'],
            close=data['last_transaction_price'],
            window=self.window
        ).cci()
        return data

    def generate_signals(self, data):
        data['Signal_cci'] = 'Hold'
        data.loc[data['cci'] < -100, 'Signal_cci'] = 'Buy'
        data.loc[data['cci'] > 100, 'Signal_cci'] = 'Sell'
        return data


# MACD Strategy
class MACDStrategy(IndicatorStrategy):
    def __init__(self, window):
        self.window = window

    def calculate(self, data):
        macd = ta.trend.MACD(data['last_transaction_price'])
        data['macd'] = macd.macd()
        data['macd_signal'] = macd.macd_signal()
        return data

    def generate_signals(self, data):
        data['Signal_macd'] = 'Hold'
        data.loc[data['macd'] > data['macd_signal'], 'Signal_macd'] = 'Buy'
        data.loc[data['macd'] < data['macd_signal'], 'Signal_macd'] = 'Sell'
        return data


# ADX Strategy
class ADXStrategy(IndicatorStrategy):
    def __init__(self, window):
        self.window = window

    def calculate(self, data):
        adx_indicator = ta.trend.ADXIndicator(
            high=data['max_price'],
            low=data['min_price'],
            close=data['last_transaction_price'],
            window=self.window
        )
        data['adx'] = adx_indicator.adx()
        data['+di'] = adx_indicator.adx_pos()
        data['-di'] = adx_indicator.adx_neg()
        return data

    def generate_signals(self, data):
        data['Signal_adx'] = 'Hold'
        data.loc[(data['+di'] > data['-di']) & (data['adx'] > 25), 'Signal_adx'] = 'Buy'
        data.loc[(data['-di'] > data['+di']) & (data['adx'] > 25), 'Signal_adx'] = 'Sell'
        return data