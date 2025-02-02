import pandas as pd
from .oscillators.oscillators import RSIStrategy, StochKStrategy, CCIStrategy, MACDStrategy, ADXStrategy
from .moving_averages.moving_averages import SMAStrategy, EMAStrategy, IchimokuBaselineStrategy
from datascraper.models import DayEntryAsString
from datascraper.serializers import DayEntryAsStringSerializer

# Constants
WINDOW = 14
SMOOTH_WINDOW = None
SHORT_TERM_WINDOW = 50
LONG_TERM_WINDOW = 200
TOTAL_ENTRIES = 2520

# Indicator Strategy
class IndicatorStrategyFactory:
    @staticmethod
    def get_strategy(indicator):
        strategies = {
            'RSI': RSIStrategy(WINDOW),
            'stoch_k': StochKStrategy(WINDOW, SMOOTH_WINDOW),
            'cci': CCIStrategy(WINDOW),
            'macd': MACDStrategy(WINDOW),
            'adx': ADXStrategy(WINDOW),
            'SMA(50)': SMAStrategy(SHORT_TERM_WINDOW),
            'SMA(200)': SMAStrategy(LONG_TERM_WINDOW),
            'EMA(50)': EMAStrategy(SHORT_TERM_WINDOW),
            'EMA(200)': EMAStrategy(LONG_TERM_WINDOW),
            'Ichimoku_Baseline': IchimokuBaselineStrategy()
        }
        return strategies.get(indicator)


class DataProcessor:
    def __init__(self, indicators, freqs=['1D', '1W', '1ME']):
        self.indicators = indicators
        self.freqs = freqs

    def process(self, company_code):
        df = self._load_data(company_code)
        self._validate_data(df)

        results = {}
        for freq in self.freqs:
            resampled_data = self._resample(df, freq)
            results[freq] = self._apply_indicators(resampled_data)
        return results

    def _load_data(self, company_code):
        entries = DayEntryAsString.objects.filter(company_code=company_code)
        serializer = DayEntryAsStringSerializer(entries, many=True)
        data = serializer.data
        df = pd.DataFrame(data)
        return self._clean_data(df)

    def _validate_data(self, df):
        missing_entries, missing_percentage = calculate_missing_entries(df)
        if missing_percentage > 20:
            raise ValueError(f"Company has too much missing data (over 20%). Skipping analysis.")
        return missing_entries, missing_percentage

    def _resample(self, df, freq):
        return resample_data(df, freq) if freq != '1D' else df

    def _apply_indicators(self, df):
        for indicator in self.indicators:
            strategy = IndicatorStrategyFactory.get_strategy(indicator)
            if strategy:
                df = strategy.calculate(df)
                df = strategy.generate_signals(df)
        return df

    def _clean_data(self, data):
        data['last_transaction_price'] = self._convert_column(data['last_transaction_price'])
        data['max_price'] = self._convert_column(data['max_price'])
        data['min_price'] = self._convert_column(data['min_price'])
        data['date'] = pd.to_datetime(data['date'], errors='coerce')
        data = data.sort_values(by='date').reset_index(drop=True).set_index('date')
        data['max_price'] = data['max_price'].ffill()
        data['min_price'] = data['min_price'].ffill()
        return data

    def _convert_column(self, column):
        column = column.str.replace('.', '').str.replace(',', '.')
        return pd.to_numeric(column, errors='coerce')


def resample_data(data, freq):
    resampled_data = data.resample(freq).agg({
        'last_transaction_price': 'mean',
        'max_price': 'max',
        'min_price': 'min'
    })
    return _handle_nulls(resampled_data, freq)

def _handle_nulls(resampled_data, freq):
    for col in ['last_transaction_price', 'max_price', 'min_price']:
        if resampled_data[col].isnull().any():
            resampled_data[col] = resampled_data[col].ffill()
            print(f'Null values found and filled for {col} in {freq}')
    return resampled_data

def calculate_missing_entries(df, total_entries=TOTAL_ENTRIES):
    actual_entries = len(df)
    missing_entries = total_entries - actual_entries
    missing_percentage = (missing_entries / total_entries) * 100
    return missing_entries, missing_percentage
