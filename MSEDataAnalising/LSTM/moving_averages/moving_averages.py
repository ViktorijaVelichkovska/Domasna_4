from LSTM.base_ta import IndicatorStrategy


class MovingAverageStrategy(IndicatorStrategy):
    def __init__(self, window_or_span, threshold=0.1, is_ema=False):
        self.window_or_span = window_or_span
        self.threshold = threshold
        self.is_ema = is_ema

    def calculate(self, data):
        if self.is_ema:
            return self._calculate_ema(data)
        else:
            return self._calculate_sma(data)

    def _calculate_sma(self, data):
        window = self.window_or_span
        if len(data) >= window:
            data[f'SMA({window})'] = data['last_transaction_price'].rolling(window=window).mean()
        else:
            small_window = int(len(data) * 0.9)
            data[f'SMA({window})'] = data['last_transaction_price'].rolling(window=small_window).mean()
        return data

    def _calculate_ema(self, data):
        span = self.window_or_span
        if len(data) >= span:
            data[f'EMA({span})'] = data['last_transaction_price'].ewm(span=span, adjust=False).mean()
        else:
            small_window = int(len(data) * 0.9)
            data[f'EMA({span})'] = data['last_transaction_price'].rolling(window=small_window).mean()
        return data

    def generate_signals(self, data):
        signal_column = self._get_signal_column_name()
        data[signal_column] = 'Hold'

        buy_condition = data['last_transaction_price'] > (1 + self.threshold) * data[self._get_ma_column_name()]
        sell_condition = data['last_transaction_price'] < (1 - self.threshold) * data[self._get_ma_column_name()]

        data.loc[buy_condition, signal_column] = 'Buy'
        data.loc[sell_condition, signal_column] = 'Sell'
        return data

    def _get_ma_column_name(self):
        return f'SMA({self.window_or_span})' if not self.is_ema else f'EMA({self.window_or_span})'

    def _get_signal_column_name(self):
        return f'Signal_{self._get_ma_column_name()}'


class IchimokuBaselineStrategy(IndicatorStrategy):
    def __init__(self, threshold=0.1):
        self.threshold = threshold

    def calculate(self, data):
        data['Ichimoku_Baseline'] = (
            data['max_price'].rolling(window=26).max() +
            data['min_price'].rolling(window=26).min()
        ) / 2
        return data

    def generate_signals(self, data):
        signal_column = 'Signal_Ichimoku_Baseline'
        data[signal_column] = 'Hold'

        buy_condition = data['last_transaction_price'] > (1 + self.threshold) * data['Ichimoku_Baseline']
        sell_condition = data['last_transaction_price'] < (1 - self.threshold) * data['Ichimoku_Baseline']

        data.loc[buy_condition, signal_column] = 'Buy'
        data.loc[sell_condition, signal_column] = 'Sell'
        return data


class IndicatorStrategyFactory:
    @staticmethod
    def get_strategy(indicator):
        strategies = {
            'SMA(50)': MovingAverageStrategy(50),
            'SMA(100)': MovingAverageStrategy(100),
            'EMA(50)': MovingAverageStrategy(50, is_ema=True),
            'EMA(100)': MovingAverageStrategy(100, is_ema=True),
            'Ichimoku_Baseline': IchimokuBaselineStrategy()
        }
        return strategies.get(indicator)
